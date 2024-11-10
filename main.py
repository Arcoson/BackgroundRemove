#!/usr/bin/env python3
import os
from pathlib import Path
from PIL import Image
from rembg import remove
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt
from rich.markdown import Markdown

console = Console()

def show_welcome():
    welcome_text = """
# 🎨 BackgroundRemove

Welcome to BackgroundRemove! This tool helps you remove backgrounds from images with ease.

## Commands:
- `remove`: Remove background from an image
- `help`: Show this help message
- `exit`: Exit the program

## Supported Formats:
- PNG
- JPEG/JPG
- WebP
"""
    console.print(Markdown(welcome_text))

def remove_background(input_path: str, output_path: str) -> bool:
    try:
        # Read input image
        input = Image.open(input_path)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Removing background...", total=100)
            
            # Remove background
            progress.update(task, advance=50)
            output = remove(input)
            
            # Save output
            progress.update(task, advance=25)
            output.save(output_path)
            progress.update(task, advance=25)
            
        return True

    except Exception as e:
        console.print(f"[red]Error during background removal: {str(e)}[/]")
        return False

def remove_command():
    input_path = Prompt.ask("Enter input image path")
    if not os.path.exists(input_path):
        console.print("[red]Error: Input file does not exist[/]")
        return

    output_path = Prompt.ask("Enter output image path (with .png extension)")
    if not output_path.lower().endswith('.png'):
        console.print("[red]Error: Output must be PNG format[/]")
        return

    console.print(Panel.fit(
        f"[bold green]Background Removal[/]\n"
        f"Processing: [cyan]{os.path.basename(input_path)}[/] → [cyan]{os.path.basename(output_path)}[/]",
        border_style="green"
    ))

    success = remove_background(input_path, output_path)

    if success:
        console.print("[green]Background removed successfully! ✨[/]")
    else:
        console.print("[red]Background removal failed! ❌[/]")

def main():
    show_welcome()
    
    while True:
        command = Prompt.ask("\nEnter command", choices=["remove", "help", "exit"])
        
        if command == "remove":
            remove_command()
        elif command == "help":
            show_welcome()
        elif command == "exit":
            console.print("[yellow]Thanks for using BackgroundRemove! Goodbye! 👋[/]")
            break

if __name__ == "__main__":
    main()
