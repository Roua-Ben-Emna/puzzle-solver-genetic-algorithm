import pygame
import sys
import tkinter as tk
from tkinter import filedialog
from genetic_algorithm import genetic_algorithm  # Import the custom genetic algorithm module

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (70, 130, 180)
RED = (255, 69, 0)
HOVER_COLOR = (100, 149, 237)
BUTTON_TEXT_COLOR = (255, 255, 255)
IMAGE_SIZE = (400, 400)  

# Function to load and resize the puzzle image
def load_puzzle_image(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

# Function to slice the image into pieces based on the grid size
def slice_image(image, grid_size):
    global TILE_SIZE  
    TILE_SIZE = image.get_width() // grid_size  # Calculate the size of each tile
    pieces = []
    for row in range(grid_size):
        for col in range(grid_size):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE) 
            piece = image.subsurface(rect).copy()  # Extract each piece as a surface
            pieces.append(piece)
    return pieces

# Adjust population size and generation count based on grid size
def adjust_parameters_for_grid_size(grid_size):
    if grid_size == 3:
        return 100, 300
    elif grid_size == 4:
        return 200, 500
    elif grid_size == 5:
        return 500, 1000

# Function to open file dialog and select an image
def choose_image():
    root = tk.Tk()
    root.withdraw()  # Hide the tkinter root window
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    
    if file_path:
        return file_path
    else:
        return None

# Draw the puzzle pieces and display fitness information
def draw_puzzle(screen, pieces, generation, fitness):
    screen.fill(BLACK) 
    for i, piece in enumerate(pieces):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        screen.blit(piece, (col * TILE_SIZE, row * TILE_SIZE))  # Place the piece on the screen
    font = pygame.font.SysFont("Arial", 24)
    text = f"Generation: {generation} | Fitness: {fitness:.2f}" # Display generation and fitness
    rendered_text = font.render(text, True, WHITE)
    screen.blit(rendered_text, (10, 10))

# Draw a gradient background    
def draw_gradient_background(screen, color1, color2):
    for i in range(IMAGE_SIZE[1]):
        blend = i / IMAGE_SIZE[1]
        r = int(color1[0] * (1 - blend) + color2[0] * blend)
        g = int(color1[1] * (1 - blend) + color2[1] * blend)
        b = int(color1[2] * (1 - blend) + color2[2] * blend)
        pygame.draw.line(screen, (r, g, b), (0, i), (IMAGE_SIZE[0], i))

# Dynamically adjust font size to fit within a given width
def adjust_font_size_to_fit(text, max_width, font_name="Arial", max_font_size=24, color=WHITE):
    font_size = max_font_size
    font = pygame.font.SysFont(font_name, font_size)
    while font.size(text)[0] > max_width and font_size > 10: 
        font_size -= 1
        font = pygame.font.SysFont(font_name, font_size)
    return font

# Draw a header with generation, fitness, and status information
def draw_header(screen, generation, fitness, status):
    header_rect = pygame.Rect(0, 0, IMAGE_SIZE[0], 50)
    pygame.draw.rect(screen, GRAY, header_rect)

    # Define maximum widths for each section of the header
    gen_max_width = 150
    fit_max_width = 150
    status_max_width = IMAGE_SIZE[0] - (gen_max_width + fit_max_width + 30)  

    gen_font = adjust_font_size_to_fit(f"Generation: {generation}", gen_max_width)
    fit_font = adjust_font_size_to_fit(f"Fitness: {fitness:.2f}", fit_max_width)
    status_font = adjust_font_size_to_fit(f"Status: {status}", status_max_width)

    # Render the text and place it on the header
    gen_surface = gen_font.render(f"Generation: {generation}", True, WHITE)
    fit_surface = fit_font.render(f"Fitness: {fitness:.2f}", True, WHITE)
    status_surface = status_font.render(f"Status: {status}", True, WHITE)

    screen.blit(gen_surface, (10, 10))
    screen.blit(fit_surface, (170, 10))  
    screen.blit(status_surface, (330, 10))  

# Draw a button with hover effects
def draw_button(screen, text, rect, color, hover_color, text_color, border_radius=10):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect, border_radius=border_radius)
    else:
        pygame.draw.rect(screen, color, rect, border_radius=border_radius)

    font = pygame.font.SysFont("Arial", 20)
    rendered_text = font.render(text, True, text_color)
    text_rect = rendered_text.get_rect(center=rect.center)
    screen.blit(rendered_text, text_rect)

# Main menu for selecting grid size
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))  
    pygame.display.set_caption("Puzzle Solver - Main Menu")
    font = pygame.font.SysFont("Arial", 36)

    running = True
    grid_size = None

    while running:
        screen.fill(GRAY)

        title = font.render("Select Grid Size", True, WHITE)
        title_rect = title.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title, title_rect.topleft)
        
        # Define buttons for each grid size
        buttons = {
            3: (pygame.Rect(screen.get_width() // 2 - 75, 180, 150, 50), "3 (Easy)"),
            4: (pygame.Rect(screen.get_width() // 2 - 75, 260, 150, 50), "4 (Medium)"),
            5: (pygame.Rect(screen.get_width() // 2 - 75, 340, 150, 50), "5 (Hard)"),
        }

        for size, (rect, label) in buttons.items():
            draw_button(screen, label, rect, BLUE, HOVER_COLOR, BUTTON_TEXT_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:   # Check button clicks
                for size, (rect, label) in buttons.items():
                    if rect.collidepoint(event.pos):  
                        grid_size = size
                        running = False

        pygame.display.flip() # Update the display

    return grid_size

# Main function
def main():
    global GRID_SIZE
    GRID_SIZE = main_menu() # Get grid size from menu

    # Let the user upload an image
    IMAGE_PATH = choose_image()  # Get the image path from file dialog
    if not IMAGE_PATH:
        print("No image selected. Exiting...")
        pygame.quit()
        sys.exit()

    global IMAGE_SIZE
    IMAGE_SIZE = (400 + GRID_SIZE * 50, 400 + GRID_SIZE * 50)  # Adjust image size based on grid size

    global POPULATION_SIZE, GENERATIONS
    POPULATION_SIZE, GENERATIONS = adjust_parameters_for_grid_size(GRID_SIZE)  # Set GA parameters

    screen = pygame.display.set_mode(IMAGE_SIZE)  
    pygame.display.set_caption("GA Puzzle Solver")  
    clock = pygame.time.Clock()

    image = load_puzzle_image(IMAGE_PATH, IMAGE_SIZE)  # Load and resize the puzzle image
    pieces = slice_image(image, GRID_SIZE)             # Slice the image into tiles
    target = pieces[:]    
    solution = None
    history = []
    status = "Solving..."

    # Solve the puzzle using the genetic algorithm
    if solution is None:
        result, history = genetic_algorithm(target, pieces, POPULATION_SIZE, GENERATIONS)

        if result == "solution_found":
            status = "Solution Found!"
        elif result == "stagnation":
            status = "Stagnation Detected."
        elif result == "no_solution":
            status = "No Solution Found."

    running = True
    current_generation = 0
    visualization_complete = False

    restart_button = pygame.Rect(10, IMAGE_SIZE[1] - 60, 120, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    main()

        draw_gradient_background(screen, GRAY, BLACK)

        # Visualize the solution generation by generation
        if not visualization_complete:
            if current_generation < len(history):
                generation, best_solution, fitness = history[current_generation]
                draw_puzzle(screen, best_solution, generation, fitness)
                draw_header(screen, generation, fitness, "Solving...")
                current_generation += 1
                clock.tick(5)
            else:
                visualization_complete = True
                print("Visualization Complete")
        else:
            # Display the final solution
            if history:
                final_generation, final_solution, final_fitness = history[-1]
            else:
                final_generation, final_solution, final_fitness = 0, target, 0

            draw_puzzle(screen, final_solution, final_generation, final_fitness)
            draw_header(screen, final_generation, final_fitness, status)

        draw_button(screen, "Restart", restart_button, RED, HOVER_COLOR, BUTTON_TEXT_COLOR)
        pygame.display.flip()
        clock.tick(30) # Limit the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
