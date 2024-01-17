import requests
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk

class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Information")

        self.create_frames()
        self.create_widgets()
        self.configure_colors()

        # Favorites list
        self.favorites = set()

    def create_frames(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack()

        self.info_frame = ttk.Frame(self.root)

    def create_widgets(self):
        # Main Page Widgets
        self.label = tk.Label(self.main_frame, text="Select Pokemon:", foreground='#2E8B57')  # SeaGreen
        self.label.grid(row=0, column=0, pady=10)

        self.pokemon_list = self.get_pokemon_list()
        self.selected_pokemon = tk.StringVar()
        self.pokemon_dropdown = ttk.Combobox(self.main_frame, textvariable=self.selected_pokemon, values=self.pokemon_list)
        self.pokemon_dropdown.grid(row=0, column=1, pady=10)

        self.button = tk.Button(self.main_frame, text="Get Info", command=self.get_pokemon_info, foreground='#2E8B57')  # SeaGreen
        self.button.grid(row=1, column=0, columnspan=2, pady=10)

        self.free_search_entry = ttk.Entry(self.main_frame)
        self.free_search_entry.grid(row=2, column=0, columnspan=2, pady=10)

        self.free_search_button = tk.Button(self.main_frame, text="Free Search", command=self.free_search_pokemon, foreground='#2E8B57')  # SeaGreen
        self.free_search_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Display Pokemon image
        self.pokemon_image_label = tk.Label(self.main_frame)
        self.pokemon_image_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Info Page Widgets
        self.back_button = ttk.Button(self.info_frame, text="Back to Main Page", command=self.show_main_page)

        self.result_text = tk.Text(self.info_frame, height=10, width=40, wrap=tk.WORD, bg='#FFE4B5', fg='#2E8B57', font=('Arial', 10))

        # Favorites Page Widgets
        self.favorites_button = tk.Button(self.main_frame, text="View Favorites", command=self.show_favorites_page, foreground='#2E8B57')  # SeaGreen
        self.favorites_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.add_to_favorites_button = tk.Button(self.main_frame, text="Add to Favorites", command=self.add_to_favorites, foreground='#2E8B57')  # SeaGreen
        self.add_to_favorites_button.grid(row=6, column=0, columnspan=2, pady=10)

    def configure_colors(self):
        # Customize the colors of the GUI
        self.root.configure(bg='#FFD700')  # LightGoldenrodYellow

    def get_pokemon_list(self):
        url = "https://pokeapi.co/api/v2/pokemon?limit=100"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [pokemon['name'].capitalize() for pokemon in data['results']]
        else:
            return ["Error"]

    def get_pokemon_info(self):
        pokemon_name = self.selected_pokemon.get() or self.free_search_entry.get()
        if pokemon_name:
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
            response = requests.get(url)
            if response.status_code == 200:
                pokemon_data = response.json()
                self.display_pokemon_info(pokemon_data)
                self.show_info_page()
            else:
                self.show_error_message(f"Error: {response.status_code}")
        else:
            self.show_error_message("Please select or enter a Pokemon")

    def display_pokemon_info(self, pokemon_data):
        self.result_text.delete(1.0, tk.END)
        name = pokemon_data['name'].capitalize()
        types = ", ".join([t['type']['name'].capitalize() for t in pokemon_data['types']])
        abilities = ", ".join([a['ability']['name'].capitalize() for a in pokemon_data['abilities']])
        stats = "\n".join([f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}" for stat in pokemon_data['stats']])
        info_text = f"Name: {name}\nTypes: {types}\nAbilities: {abilities}\nStats:\n{stats}"
        self.result_text.insert(tk.END, info_text)

        # Display Pokemon image
        self.display_pokemon_image(pokemon_data['id'])

    def display_pokemon_image(self, pokemon_id):
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image_data = Image.open(response.raw)
            image_data = ImageTk.PhotoImage(image_data)
            self.pokemon_image_label.configure(image=image_data)
            self.pokemon_image_label.image = image_data
        else:
            self.pokemon_image_label.configure(text="Image not available")

    def show_info_page(self):
        self.main_frame.pack_forget()
        self.info_frame.pack()
        self.back_button.pack(side=tk.TOP)
        self.result_text.pack()

    def show_main_page(self):
        self.info_frame.pack_forget()
        self.main_frame.pack()

    def free_search_pokemon(self):
        self.pokemon_dropdown.set('')
        self.get_pokemon_info()

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def show_favorites_page(self):
        favorites_window = tk.Toplevel(self.root)
        favorites_window.title("Favorite Pokemon")

        favorites_label = tk.Label(favorites_window, text="Favorite Pokemon", foreground='#2E8B57', font=('Arial', 14, 'bold'))  # SeaGreen
        favorites_label.pack(pady=10)

        favorites_listbox = tk.Listbox(favorites_window, selectmode=tk.MULTIPLE, bg='#FFE4B5', fg='#2E8B57', font=('Arial', 12))
        for pokemon in sorted(self.favorites):
            favorites_listbox.insert(tk.END, pokemon)
        favorites_listbox.pack(pady=10)

        remove_button = tk.Button(favorites_window, text="Remove Selected", command=lambda: self.remove_from_favorites(favorites_listbox.curselection()), foreground='#2E8B57')  # SeaGreen
        remove_button.pack(pady=10)

    def add_to_favorites(self):
        selected_pokemon = self.selected

    def add_to_favorites(self):
        selected_pokemon = self.selected_pokemon.get()
        if selected_pokemon:
            self.favorites.add(selected_pokemon)
            messagebox.showinfo("Success", f"{selected_pokemon.capitalize()} added to favorites!")
        else:
            self.show_error_message("Please select or enter a Pokemon")

    def remove_from_favorites(self, selected_indices):
        if selected_indices:
            selected_pokemon = [sorted(self.favorites)[index] for index in selected_indices]
            for pokemon in selected_pokemon:
                self.favorites.remove(pokemon)
            messagebox.showinfo("Success", "Selected Pokemon removed from favorites!")
        else:
            self.show_error_message("Please select a Pokemon to remove")

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)

    root.mainloop()
