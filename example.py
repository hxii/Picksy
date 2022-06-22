from picksy import Picksy

food_options = {
    "hamburger": "Hamburger and Fries",
    "hamburger_soda": "Hamburger and Fries incl. Soda",
    "fish_n_chips": "Fish and Chips",
    "sushi": "Sushi",
    "pizza": "Pizza",
    "fruit": "Fruit Platter",
}

menu = Picksy(food_options, "Pick some food to go with the movie:\n")

print(f"Your choice was {menu.get_choice()}")
