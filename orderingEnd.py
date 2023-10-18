from datetime import date
import time
from tkinter import Tk, Label, Button, Frame, Canvas, Scrollbar
from PIL import ImageTk, Image
import tkinter.font as tkfont
import socket

item_selections = {}
username = "5"

host = "000.000.000.000"  # The IPv4 address of the server hosting computer
port = 9999  # Data type should be int


def send_order_message(item_list):
    # Establish a connection to the server
    server_address = (host, port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    # Prepare the order message
    order_message = ','.join(item_list)

    client_socket.sendall(order_message.encode('utf-8'))
    print(f"Message sent: {order_message}")


# Function to handle item selection
def item_clicked(event, item_id, amount_label):
    if item_id in item_selections:
        item_selections[item_id] += 1
    else:
        item_selections[item_id] = 1
    update_amount_label(amount_label, item_id)

# Function to handle removing item selection


def remove_item_clicked(event, item_id, amount_label):
    if item_id in item_selections:
        item_selections[item_id] -= 1
        if item_selections[item_id] <= 0:
            del item_selections[item_id]
    update_amount_label(amount_label, item_id)


# Function to update the "Amount Selected" label
def update_amount_label(amount_label, item_id):
    amount_label.config(
        text=f"Quantity: {item_selections.get(item_id, 0)}")


def place_order(root):
    final_list = [username, "order msg"]
    prices = []
    items = []
    i = 0
    for x in menu_items.values():
        i += 1
        s = str(i)
        if s in item_selections:
            final_list.append(x['name'])
            final_list.append(str(item_selections[s]))
            prices.append([f"{x['price']}", f"{item_selections[s]}"])
            items.append(x["name"])
        else:
            pass
    send_order_message(final_list)
    calcCost(prices, items, root)
    item_selections.clear()


def calcCost(prices, items, root):
    prices = [[int(y) for y in x] for x in prices]
    prices2 = prices.copy()

    grandTotal = 0
    for z in range(len(prices)):
        grandTotal += prices[z][0]*prices[z][1]
    grandTotalRupees = f"₹{grandTotal}"
    pricesOnly = []
    qty = []
    for a in prices2:
        b, c = a
        pricesOnly.append(int(b))
        qty.append(int(c))
    root.destroy()
    postOrder(grandTotalRupees, items, qty, pricesOnly)


def postOrder(grandTotal, items, qty, prices):
    postOrderScreen = Tk()
    postOrderScreen.title("Bill")
    postOrderScreen.geometry("625x7254")
    postOrderScreen.config(background="#0A3C57")

    Label(postOrderScreen, bg="#0A3C57", text="YOUR ORDER WILL ARRIVE SHORTLY!", font=tkfont.Font(
        family="Berlin Sans FB Demi", size=22), fg="white").pack(anchor="center", pady=(10, 25))

    invoiceFrame = Frame(postOrderScreen, bg="#FFFFFF")
    invoiceFrame.pack(fill="both", anchor="center", padx=50)

    invoiceLabel = Label(invoiceFrame, text="INVOICE", font=tkfont.Font(
        family="Roboto", size=36, weight="bold"), bg="#FFFFFF", fg="#0A4F66")
    invoiceLabel.grid(row=0, sticky="new")

    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    today = date.today()
    dateLabel = Label(invoiceFrame, text=f"Date: {today}", font=tkfont.Font(
        family="Roboto", size=12, weight="bold"), bg="#FFFFFF", fg="#000000")
    dateLabel.grid(row=2, column=0, sticky="w")

    timeLabel = Label(invoiceFrame, text=f"Time: {current_time}", font=tkfont.Font(
        family="Roboto", size=12, weight="bold"), bg="#FFFFFF", fg="#000000")
    timeLabel.grid(row=3, column=0, sticky="w")

    tableLabel = Label(invoiceFrame, text=f"Table No. {username}", font=tkfont.Font(
        family="Roboto", size=12, weight="bold"), bg="#FFFFFF", fg="#000000")
    tableLabel.grid(row=4, column=0, sticky="w")

    divider = Label(invoiceFrame, text="____________________________________________________________________________________________________________",
                    bg="#FFFFFF", fg="#000000")

    divider.grid(row=5, sticky="new")

    categoryFrame = Frame(invoiceFrame, bg="#CFECEF")
    categoryFrame.grid(row=7, sticky="new")

    descriptionLabel = Label(categoryFrame, text="Description", font=tkfont.Font(
        family="Roboto", size=12, weight="bold"), bg="#CFECEF", fg="#000000")
    descriptionLabel.grid(row=7, column=0, sticky="w", padx=(0, 270))

    qtyLabel = Label(categoryFrame, text="Qty", font=tkfont.Font(family="Roboto", size=12, weight="bold"),
                     bg="#CFECEF", fg="#000000")
    qtyLabel.grid(row=7, column=1, padx=(0, 15))

    priceLabel = Label(categoryFrame, text="Price", font=tkfont.Font(family="Roboto", size=12, weight="bold"),
                       bg="#CFECEF", fg="#000000")
    priceLabel.grid(row=7, column=2, padx=(5, 15))

    totalLabel = Label(categoryFrame, text="Total", font=tkfont.Font(family="Roboto", size=12, weight="bold"),
                       bg="#CFECEF", fg="#000000")
    totalLabel.grid(row=7, column=3, padx=(5, 0))

    e = 8
    for x in range(len(prices)):
        f = e + x
        food_name = items[x]
        quantity = qty[x]
        unitPrice = prices[x]

        qtyPriceTotalsFrame = Frame(invoiceFrame, bg="#FFFFFF")
        qtyPriceTotalsFrame.grid(row=f, column=0, sticky="nse", padx=(0, 25))

        itemLabel = Label(invoiceFrame, text=food_name, font=tkfont.Font(family="Roboto", size=12, weight="bold"),
                          bg="#FFFFFF", fg="#000000")

        itemLabel.grid(row=f, column=0, sticky="nw")

        strUnitPrice = str(unitPrice)
        l = 0
        for k in strUnitPrice:
            l += 1
        if l == 2:
            m = 41
        elif l == 3:
            m = 30
        elif l == 4:
            m = 22
        elif l == 5:
            m = 13

        quantityLabel = Label(qtyPriceTotalsFrame, text=quantity, font=tkfont.Font(family="Roboto", size=12, weight="bold"),
                              bg="#FFFFFF", fg="#000000")
        quantityLabel.grid(row=f, column=1, padx=(0, m))

        unitPriceLabel = Label(qtyPriceTotalsFrame, text=unitPrice, font=tkfont.Font(family="Roboto", size=12, weight="bold"),
                               bg="#FFFFFF", fg="#000000")
        unitPriceLabel.grid(row=f, column=2, padx=(5, 13))

        ItemTotal = unitPrice*quantity
        strItemTotal = str(ItemTotal)
        h = 0
        for g in strItemTotal:
            h += 1
        if h == 2:
            j = 25
        elif h == 3:
            j = 17
        elif h == 4:
            j = 8
        elif h == 5:
            j = 0
        totalLabel = Label(qtyPriceTotalsFrame, text=ItemTotal, font=tkfont.Font(family="Roboto", size=12, weight="bold"),
                           bg="#FFFFFF", fg="#0A4F66")
        totalLabel.grid(row=f, column=3, padx=(j, 0))

    grandTotalFrame = Frame(invoiceFrame, bg="#FFFFFF")
    grandTotalFrame.grid(row=f+1, column=0)
    grandTotalLabel = Label(invoiceFrame, text=grandTotal, font=tkfont.Font(family="Roboto", size=18, weight="bold"),
                            bg="#FFFFFF", fg="#0A4F66")
    grandTotalLabel.grid(sticky="e", padx=(0, 20))

    restartProgramButtonFrame = Frame(postOrderScreen, background="#0A3C57")
    restartProgramButtonFrame.pack(fill="x")
    restartProgramButton = Button(restartProgramButtonFrame, background="#232F3E", command=orderSelectionScreen, relief="raised",
                                  text="Order More Food!",
                                  font=tkfont.Font(family="Bahnschrift", size=18), fg="#FFFFFF")
    restartProgramButton.pack(fill="x", padx=50)


menu_items = {
    '1': {'name': 'Pav Bhaji', 'image': 'pavbhaji.jpg', 'price': 140, 'rating': 4},
    '2': {'name': 'Masala Dosa', 'image': 'ravamasaladosa.jpg', 'price': 160, 'rating': 4.5},
    '3': {'name': 'Mint Mojito', 'image': 'mojito.jpg', 'price': 45, 'rating': 4},
    '4': {'name': 'Chhole Bhature', 'image': 'chholebhature.jpg', 'price': 125, 'rating': 5},
    '5': {'name': 'White Sauce Pasta', 'image': 'whitesaucepasta.jpg', 'price': 260, 'rating': 5},
}

starRatings = {
    1: "1star.png",
    1.5: "1.5star.png",
    2: "2star.png",
    2.5: "2.5star.png",
    3: "3star.png",
    3.5: "3.5star.png",
    4: "4star.png",
    4.5: "4.5star.png",
    5: "5star.png"
}


def orderSelectionScreen():
    # Create the GUI window
    root = Tk()
    root.title("Menu")
    root.geometry("625x725")
    root.config(background="#FFFFFF")
    root.wm_attributes("-topmost", True)

    # Create a frame to hold the menu items
    menu_frame = Frame(root, background="#232F3E")
    menu_frame.pack(fill='both', expand=True)

    # Create a canvas for the menu items with a scrollbar
    canvas = Canvas(menu_frame, background="#FFFFFF")
    scrollbar = Scrollbar(menu_frame, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y', padx=10, pady=10)
    canvas.pack(side='left', fill='both', expand=True)

    # Create a frame inside the canvas to hold the menu items
    items_frame = Frame(canvas, background="#E7F9FF")
    canvas.create_window((0, 0), width=612, window=items_frame, anchor='nw')

    # Display menu items with images
    for item_id, item in menu_items.items():
        image_path = item['image']
        item_name = item['name']

        # Open the image using PIL
        image = Image.open(image_path)
        # Resize the image if needed
        # Adjust the image size as per your preference
        image = image.resize((470, 412))

        # Create a frame for each item
        item_frame = Frame(items_frame, background="#FFFFFF",
                           relief="solid", bd=10, padx=10, pady=10, name=item_id)
        item_frame.pack(fill='both', pady=10, padx=40, expand=True, side='top')
        item_frame.config(borderwidth=2)

        # Create a frame to hold the item details and buttons
        details_frame = Frame(item_frame, background="#FFFFFF")
        details_frame.pack(fill='x', side='bottom')

        # Bind click event to the item frame
        amount_label = Label(details_frame, text="Quantity: 0", font=tkfont.Font(family='Canva Sans', size=16, weight="bold"),
                             bg="#FFFFFF", fg="#EF233C")
        amount_label.pack(side="left")

        item_frame.bind('<Button-1>', lambda event, id=item_id,
                        label=amount_label: item_clicked(event, id, label))

        # Create a label to display the item name
        name_label = Label(item_frame, text=item_name, font=tkfont.Font(family='Canva Sans', size=24, weight="bold"),
                           bg="#FFFFFF", fg="#FF4242")
        name_label.pack(side="top", anchor='w', padx=10)

        costAndRatingsFrame = Frame(item_frame, background="#FFFFFF")
        costAndRatingsFrame.pack(fill="x")

        costLabel = Label(costAndRatingsFrame,
                          text=f"₹{item['price']}", background="#FFFFFF", foreground="#FF4242", font=tkfont.Font(family='Canva Sans', size=14))
        costLabel.pack(side="left", anchor="w", padx=10)

        rating = item['rating']
        actualRating = starRatings[rating]

        ratingsImage_path = actualRating
        ratingsImage = Image.open(ratingsImage_path)
        ratingsImage = ratingsImage.resize((137, 25))

        ratingLabel = Label(costAndRatingsFrame, background="#FFFFFF")
        ratingLabel.pack(side="right", padx=10)
        dispRating = ImageTk.PhotoImage(ratingsImage)
        ratingLabel.configure(image=dispRating)
        ratingLabel.image = dispRating

        # Create a label to display the image
        image_label = Label(item_frame, background="#FFFFFF")
        image_label.pack(side='left', padx=10, pady=10)

        # Create a PhotoImage object from the PIL image
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo

        select_button_frame = Frame(details_frame, background="#FFFFFF")
        select_button_frame.pack(side="right", padx=10)

        # Create circle buttons for selection
        select_button = Button(select_button_frame, text="+", font=tkfont.Font(family='Canva Sans', size=16),
                               command=lambda id=item_id, label=amount_label: item_clicked(
            None, id, label),
            bg="#47ABD8", fg="#FFFFFF", relief='flat', padx=30)
        select_button.pack(side='left', padx=5, pady=5)

        remove_button = Button(select_button_frame, text="-", font=tkfont.Font(family='Canva Sans', size=16),
                               command=lambda id=item_id, label=amount_label: remove_item_clicked(
            None, id, label),
            bg="#47ABD8", fg="#FFFFFF", relief='flat', padx=30)
        remove_button.pack(side='left', padx=5, pady=5)

        # Update the canvas scroll region after adding each item
        canvas.configure(scrollregion=canvas.bbox('all'))

    empty_frame = Frame(items_frame, background="#E7F9FF")
    empty_frame.pack(fill="both")

    empty_text = Label(empty_frame, background="#E7F9FF",
                       fg="#E7F9FF", text="O", font=tkfont.Font(size=76))
    empty_text.pack()

    # Create the order button
    order_button = Button(canvas, text="Place Order", font=tkfont.Font(family='Canva Sans', size=24),
                          command=lambda: place_order(root), bg="#47ABD8", fg="#FFFFFF", padx=20, pady=10)
    order_button.pack(side='bottom', padx=10, pady=(0, 15), anchor='se')

    # Bind the scrollbar to the canvas
    canvas.bind('<Configure>', lambda e: canvas.configure(
        scrollregion=canvas.bbox('all')))

    # Start the GUI event loop
    root.mainloop()


orderSelectionScreen()
