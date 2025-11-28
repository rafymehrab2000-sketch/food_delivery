import flet as ft
import asyncio

def main(page: ft.Page):
    page.title = "Food Delivery App"
    page.theme_mode = "light"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.window_full_screen = True
    page.window_maximized = True
    page.update()

    BG_IMAGE = "https://stock.adobe.com/search?k=bright+white+background"

    # -----------------------------
    # FOOD DATA
    # -----------------------------
    foods = {
        "Burger": {"name": "Burger", "price": 5.99, "image": "https://images.unsplash.com/photo-1550547660-d9450f859349"},
        "Pizza": {"name": "Pizza", "price": 8.49, "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Supreme_pizza.jpg/1200px-Supreme_pizza.jpg"},
        "Sushi": {"name": "Sushi", "price": 12.99, "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBlSDCvX8XnpmcNJHNYo_sQmXiv7tiUDkdOw&s"},
        "Taco": {"name": "Taco", "price": 4.75, "image": "https://danosseasoning.com/wp-content/uploads/2022/03/Beef-Tacos-1024x767.jpg"},
        "Salad": {"name": "Salad", "price": 6.50, "image": "https://cdn.loveandlemons.com/wp-content/uploads/2021/04/green-salad.jpg"},
        "Pasta": {"name": "Pasta", "price": 9.25, "image": "https://images.unsplash.com/photo-1525755662778-989d0524087e"},
        "Kebap": {"name": "Kebap", "price": 10.99, "image": "https://img.lovepik.com/photo/48013/2991.jpg_wh860.jpg"},
        "Lahmacun": {"name": "Lahmacun", "price": 7.50, "image": "https://img.freepik.com/free-photo/meat-lahmacun-with-green-lemon_140725-4822.jpg"},
        "Baklava": {"name": "Baklava", "price": 5.99, "image": "https://www.shutterstock.com/image-photo/middle-eastern-sweets-baklava-pistachio-600nw-2524572645.jpg"},
        "Dolma": {"name": "Dolma", "price": 6.25, "image": "https://t4.ftcdn.net/jpg/03/68/80/51/360_F_368805186_qExV5dPfimCgjVnRXpROyqDgsSk75zhm.jpg"},
        "Pide": {"name": "Pide", "price": 8.99, "image": "https://media.istockphoto.com/id/1155362263/photo/traditional-turkish-cuisine-turkish-pizza-pita-with-a-different-stuffing-meat-cheese-slices.jpg?s=612x612&w=0&k=20&c=4pNeTu9kCeJ_VQ62wJDFBPczHujJEDxnfBe0ry99KDs="},
        "Börek": {"name": "Börek", "price": 4.99, "image": "https://www.shutterstock.com/image-photo/crunchy-water-lasagna-sheets-adana-600nw-2229821991.jpg"},
    }

    # -----------------------------
    # RESTAURANTS
    # -----------------------------
    restaurants = {
        "BURGER VALLEY": ["Burger", "Pizza", "Taco"],
        "PIZZABURG": ["Pizza", "Burger", "Sushi", "Pasta"],
        "SAKURA SUSHI": ["Sushi", "Salad"],
        "TACO BELL": ["Taco", "Pasta", "Burger"],
        "TURKISH RAVINTOLA": ["Kebap", "Lahmacun", "Baklava", "Dolma", "Pide", "Börek"],
    }

    # -----------------------------
    # STATE
    # -----------------------------
    current_restaurant: str | None = None
    selected_restaurant_text = ft.Text("Select A Restaurant", size=28, weight=ft.FontWeight.BOLD)
    food_display_row = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=15, wrap=True)
    search_field = ft.TextField(label="Search menu (within selected restaurant)", width=360)
    cart: dict[str, dict] = {}
    cart_items_column = ft.Column(expand=True)
    total_text = ft.Text("Total: $0.00", size=18, weight=ft.FontWeight.BOLD)

    def show_cart():
        update_cart_view()
        container.content = cart_page()
        page.update()

    cart_button = ft.ElevatedButton(
        text="View Cart (0)",
        on_click=lambda e: show_cart(),
        style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_700, color=ft.Colors.WHITE),
    )

    # -----------------------------
    # CART FUNCTIONS
    # -----------------------------
    def update_cart_label():
        total_items = sum(info["quantity"] for info in cart.values())
        cart_button.text = f"View Cart ({total_items})"
        page.update()

    def update_cart_view():
        cart_items_column.controls.clear()
        if not cart:
            cart_items_column.controls.append(ft.Text("Your cart is empty.", size=16, color="black"))
        else:
            for name, info in cart.items():
                restaurant = info.get("restaurant", "Unknown")
                cart_items_column.controls.append(
                    ft.Row(
                        [
                            ft.Text(f"{name} - ${info['food']['price']:.2f} (from {restaurant})", size=16, color="black"),
                            ft.Row(
                                [
                                    ft.IconButton(icon=ft.Icons.REMOVE, on_click=lambda e, n=name: decrease_quantity(n)),
                                    ft.Text(str(info["quantity"]), size=16, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.IconButton(icon=ft.Icons.ADD, on_click=lambda e, n=name: increase_quantity(n)),
                                ],
                                spacing=5,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )
        total = sum(info["food"]["price"] * info["quantity"] for info in cart.values())
        total_text.value = f"Total: ${total:.2f}"
        page.update()

    def add_to_cart(food, restaurant_name):
        if food["name"] in cart:
            cart[food["name"]]["quantity"] += 1
        else:
            cart[food["name"]] = {"food": food, "quantity": 1, "restaurant": restaurant_name}
        update_cart_label()
        page.snack_bar = ft.SnackBar(ft.Text(f"Added {food['name']} from {restaurant_name} to cart!"), open=True)
        page.update()
        update_cart_view()

    def increase_quantity(name):
        cart[name]["quantity"] += 1
        update_cart_label()
        update_cart_view()

    def decrease_quantity(name):
        if cart[name]["quantity"] > 1:
            cart[name]["quantity"] -= 1
        else:
            del cart[name]
        update_cart_label()
        update_cart_view()

    # -----------------------------
    # SEARCH / FILTER
    # -----------------------------
    def filter_foods(e=None):
        if not current_restaurant:
            food_display_row.controls.clear()
            food_display_row.controls.append(ft.Text("Please select a restaurant first.", size=16, color="black"))
            page.update()
            return
        query = (search_field.value or "").strip().lower()
        food_display_row.controls.clear()
        for food_name in restaurants[current_restaurant]:
            if query and query not in food_name.lower():
                continue
            f = foods[food_name]
            card = ft.Card(
                elevation=3,
                content=ft.Column(
                    [
                        ft.Image(src=f["image"], width=180, height=120, fit=ft.ImageFit.COVER),
                        ft.Text(f["name"], size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(f"${f['price']:.2f}", size=16, color=ft.Colors.GREEN_700),
                        ft.ElevatedButton(
                            text="🛒 Add to Cart",
                            on_click=lambda e, food=f, rest=current_restaurant: add_to_cart(food, rest),
                            style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_700, color=ft.Colors.WHITE),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
            )
            food_display_row.controls.append(card)
        page.update()

    search_field.on_change = filter_foods

    def show_food_items(restaurant_name):
        nonlocal current_restaurant
        current_restaurant = restaurant_name
        selected_restaurant_text.value = restaurant_name
        search_field.value = ""
        filter_foods()

    # -----------------------------
    # ORDER COMPLETE ANIMATION (FIXED)
    # -----------------------------
    # Start with empty content so switching to image triggers animation
    confetti = ft.AnimatedSwitcher(
        content=ft.Container(),  # initially empty
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=500,
    )

    async def show_order_complete_animation():
        # Switch in: show confetti image (fade in)
        confetti.content = ft.Image(
            src="https://cdn-icons-png.flaticon.com/512/1055/1055646.png",
            width=120,
            height=120,
        )
        page.update()
        await asyncio.sleep(3)
        # Switch out: hide it again (fade out)
        confetti.content = ft.Container()
        page.update()

    def go_to_order_complete():
        cart.clear()
        update_cart_label()
        update_cart_view()
        container.content = order_complete_page
        page.update()
        page.run_task(show_order_complete_animation())

    # -----------------------------
    # RESTAURANT BUTTONS
    # -----------------------------
    restaurant_buttons = ft.Row(
        [ft.ElevatedButton(name, on_click=lambda e, n=name: show_food_items(n)) for name in restaurants.keys()],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
    )

    # -----------------------------
    # HOME BUTTON
    # -----------------------------
    def show_home():
        container.content = home_page_container()
        page.update()

    home_button = ft.IconButton(
        icon=ft.Icons.HOME,
        tooltip="Home",
        on_click=lambda e: show_home()
    )

    # -----------------------------
    # PAGES WITH FULLSCREEN BG
    # -----------------------------
    def home_page_container():
        return ft.Container(
            expand=True,
            image=ft.DecorationImage(src=BG_IMAGE, fit=ft.ImageFit.COVER),
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        [
                            home_button,
                            ft.Text(
                                "🍽 Choose Your Restaurant",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color="black",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    ft.Divider(height=8, color="transparent"),
                    restaurant_buttons,
                    ft.Divider(color="transparent"),
                    selected_restaurant_text,
                    search_field,
                    ft.Divider(color="transparent"),
                    food_display_row,
                    ft.Row([cart_button], alignment=ft.MainAxisAlignment.END),
                ]
            )
        )

    def cart_page():
        return ft.Container(
            expand=True,
            image=ft.DecorationImage(src=BG_IMAGE, fit=ft.ImageFit.COVER),
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        [
                            home_button,
                            ft.Text("🛒 Your Cart", size=26, weight=ft.FontWeight.BOLD, color="white"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    ft.Divider(color="transparent"),
                    cart_items_column,
                    ft.Divider(color="transparent"),
                    total_text,
                    ft.Row(
                        [
                            ft.ElevatedButton("⬅ Back to Menu", on_click=lambda e: show_home()),
                            ft.ElevatedButton("Proceed to Pay 💳", on_click=lambda e: go_to_order_complete()),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ]
            )
        )

    order_complete_page = ft.Container(
        expand=True,
        image=ft.DecorationImage(src=BG_IMAGE, fit=ft.ImageFit.COVER),
        content=ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Row([home_button], alignment=ft.MainAxisAlignment.START),
                confetti,
                ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_600, size=120),
                ft.Text("Order Completed!", size=30, weight=ft.FontWeight.BOLD, color="orange"),
                ft.Text("Thank you for your order! Your food is on the way 🚗💨", size=18, color="orange"),
                ft.Row(
                    [ft.ElevatedButton("Back to Menu", on_click=lambda e: show_home())],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
            ]
        )
    )

    # -----------------------------
    # MAIN CONTAINER
    # -----------------------------
    container = ft.Container(content=home_page_container(), expand=True)
    page.add(container)


ft.app(target=main)
