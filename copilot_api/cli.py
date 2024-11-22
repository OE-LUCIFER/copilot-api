#!/usr/bin/env python3
"""Command Line Interface for Copilot API."""

import click
import json
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint

from .copilot import Copilot
from .utils import save_conversation, load_conversation
from .exceptions import CopilotException

console = Console()

def print_welcome():
    """Print welcome message."""
    welcome_text = """
# 🤖 Copilot CLI

Welcome to the Copilot CLI! Type your message or use these commands:
- /help - Show this help message
- /clear - Clear the conversation
- /save <filename> - Save conversation
- /load <filename> - Load conversation
- /image <path> - Send an image (May not work)
- /exit - Exit the CLI
    """
    console.print(Markdown(welcome_text))

@click.group()
def cli():
    """Copilot API command line interface."""
    pass

@cli.command()
@click.option('--model', default='Copilot', help='Model to use for chat.')
@click.option('--save', help='Save conversation to file.')
@click.option('--load', help='Load conversation from file.')
def chat(model, save, load):
    """Start an interactive chat session."""
    copilot = Copilot()
    conversation = None
    messages = []

    if load:
        try:
            conversation = load_conversation(load)
            console.print(f"[green]Loaded conversation from {load}[/green]")
        except Exception as e:
            console.print(f"[red]Error loading conversation: {e}[/red]")

    print_welcome()

    while True:
        try:
            user_input = Prompt.ask("\n[bold blue]You[/bold blue]")

            if user_input.startswith('/'):
                if user_input == '/exit':
                    if save:
                        save_conversation(save, messages)
                        console.print(f"[green]Conversation saved to {save}[/green]")
                    break
                elif user_input == '/help':
                    print_welcome()
                    continue
                elif user_input == '/clear':
                    messages = []
                    conversation = None
                    console.print("[yellow]Conversation cleared[/yellow]")
                    continue
                elif user_input.startswith('/save '):
                    filename = user_input.split(' ')[1]
                    save_conversation(filename, messages)
                    console.print(f"[green]Conversation saved to {filename}[/green]")
                    continue
                elif user_input.startswith('/load '):
                    filename = user_input.split(' ')[1]
                    try:
                        conversation = load_conversation(filename)
                        console.print(f"[green]Loaded conversation from {filename}[/green]")
                    except Exception as e:
                        console.print(f"[red]Error loading conversation: {e}[/red]")
                    continue
                elif user_input.startswith('/image '):
                    image_path = user_input.split(' ')[1]
                    if not os.path.exists(image_path):
                        console.print("[red]Image file not found[/red]")
                        continue
                    messages.append({"role": "user", "content": "Here's an image to analyze:"})
                    console.print("[yellow]Sending image...[/yellow]")
                    response_text = ""
                    for response in copilot.create_completion(
                        model=model,
                        messages=messages,
                        stream=True,
                        image=image_path,
                        conversation=conversation
                    ):
                        if isinstance(response, str):
                            response_text += response
                            console.print(response, end="")
                    messages.append({"role": "assistant", "content": response_text})
                    continue

            messages.append({"role": "user", "content": user_input})
            response_text = ""
            
            console.print("\n[bold green]Assistant[/bold green]")
            for response in copilot.create_completion(
                model=model,
                messages=messages,
                stream=True,
                conversation=conversation
            ):
                if isinstance(response, str):
                    response_text += response
                    console.print(response, end="")
            
            messages.append({"role": "assistant", "content": response_text})
            console.print("\n")

        except CopilotException as e:
            console.print(f"\n[red]Error: {e}[/red]")
        except KeyboardInterrupt:
            if save:
                save_conversation(save, messages)
                console.print(f"\n[green]Conversation saved to {save}[/green]")
            break
        except Exception as e:
            console.print(f"\n[red]Unexpected error: {e}[/red]")

@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--model', default='Copilot', help='Model to use for image analysis.')
def analyze_image(image_path, model):
    """Analyze an image using Copilot."""
    copilot = Copilot()
    messages = [{"role": "user", "content": "What's in this image?"}]

    try:
        console.print("[yellow]Analyzing image...[/yellow]")
        response_text = ""
        for response in copilot.create_completion(
            model=model,
            messages=messages,
            stream=True,
            image=image_path
        ):
            if isinstance(response, str):
                response_text += response
                console.print(response, end="")
        console.print("\n")
    except Exception as e:
        console.print(f"[red]Error analyzing image: {e}[/red]")

@cli.command()
def export(format: str = 'json'):
    """Export conversation history to different formats."""
    try:
        if format.lower() not in ['json', 'txt', 'md']:
            raise click.BadParameter("Format must be one of: json, txt, md")
        
        filename = f"conversation_export.{format}"
        conversation = load_conversation("latest.json")
        
        if format == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(conversation, f, indent=2)
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                for msg in conversation:
                    if format == 'md':
                        f.write(f"## {msg['role'].title()}\n{msg['content']}\n\n")
                    else:
                        f.write(f"{msg['role']}: {msg['content']}\n")
        
        console.print(f"[green]Conversation exported to {filename}[/green]")
    except Exception as e:
        console.print(f"[red]Error exporting conversation: {str(e)}[/red]")

@cli.command()
def summarize():
    """Summarize the current conversation."""
    try:
        conversation = load_conversation("latest.json")
        copilot = Copilot()
        
        summary_prompt = "Please provide a concise summary of this conversation, highlighting the main points discussed:"
        for msg in conversation[-10:]:  # Get last 10 messages for summary
            summary_prompt += f"\n{msg['role']}: {msg['content']}"
        
        messages = [{"role": "user", "content": summary_prompt}]
        response = copilot.create_completion(model="Copilot", messages=messages)
        
        console.print(Panel(Markdown(response), title="Conversation Summary", border_style="blue"))
    except Exception as e:
        console.print(f"[red]Error summarizing conversation: {str(e)}[/red]")

@cli.command()
def system():
    """Display system information and configuration."""
    import platform
    import sys
    from . import __version__
    
    info = {
        "Python Version": sys.version.split()[0],
        "Platform": platform.platform(),
        "Copilot CLI Version": __version__,
        "Default Model": "Copilot",
    }
    
    console.print(Panel(
        "\n".join([f"{k}: {v}" for k, v in info.items()]),
        title="System Information",
        border_style="green"
    ))

@cli.command()
@click.option('--persona', help='Set a custom chat persona/style.')
@click.option('--temperature', type=float, help='Set response creativity (0.0-1.0).')
@click.option('--context', help='Set custom context for the conversation.')
def configure(persona, temperature, context):
    """Configure chat settings and persona."""
    config = {}
    
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
    
    if persona:
        config['persona'] = persona
    if temperature is not None:
        config['temperature'] = max(0.0, min(1.0, temperature))
    if context:
        config['context'] = context
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    console.print("[green]Configuration updated successfully![/green]")
    console.print(Panel(
        "\n".join([f"{k}: {v}" for k, v in config.items()]),
        title="Current Configuration",
        border_style="blue"
    ))

if __name__ == '__main__':
    cli()
