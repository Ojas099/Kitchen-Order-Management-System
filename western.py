from tkinter import Tk, Label, Frame
import tkinter.font as tkfont
import socket
import threading

host = 'xxx.xxx.xxx.xxx'
port = 9999
username = "Western"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def usernameDeclaration(client):
    message_type = "username declaration"
    msg = [username, message_type]
    final_msg = ','.join(msg)
    client.sendall(final_msg.encode('utf-8'))


def kitchenInterface(tableNum, orders_list, orders_qty):
    root = Tk()
    root.title("Orders")
    root.attributes("-fullscreen", True)
    root.config(bg="#131921")

    table_no = tableNum[-1]

    headerLabel = Label(root, text="Continental Orders:", font=tkfont.Font(
        family="Arial Rounded MT Bold", size=42), fg="#FFFFFF", bg="#131921")
    headerLabel.pack(side="top", anchor="nw", padx="35")

    ordersFrame = Frame(root, bg="#202A36", relief="raised", bd=10)
    ordersFrame.pack(side="top", anchor="center",
                     padx=35, pady=15, fill="both")

    # All Labels in the topmost line defining categories
    itemCategory = Label(ordersFrame, text="Items", font=tkfont.Font(
        family="Cambria", size=20), fg="#B1CB5A", bg="#202A36")
    itemCategory.grid(row=0, column=0, sticky="w")

    ordersFrame.grid_columnconfigure(1, minsize=885)

    qtyCategory = Label(ordersFrame, text="Qty", font=tkfont.Font(
        family="Cambria", size=20), fg="#B1CB5A", bg="#202A36")
    qtyCategory.grid(row=0, column=2)

    ordersFrame.grid_columnconfigure(3, minsize=40)

    tableCategory = Label(ordersFrame, text="Table_No", font=tkfont.Font(
        family="Cambria", size=20), fg="#B1CB5A", bg="#202A36")
    tableCategory.grid(row=0, column=4, sticky="e")

    list_pos = 0
    loop_count = len(orders_list) + 2

    for xyz in range(2, loop_count):
        current_order = orders_list[list_pos]
        current_qty = orders_qty[list_pos]

        itemLabel = Label(ordersFrame, text=current_order, bg="#202A36",
                          fg="#FFFFFF", font=tkfont.Font(family="Arial Rounded MT Bold", size=16))
        itemLabel.grid(row=xyz, column=0, sticky="w")

        qtyLabel = Label(ordersFrame, text=current_qty, bg="#202A36", fg="#FFFFFF",
                         font=tkfont.Font(family="Arial Rounded MT Bold", size=16))
        qtyLabel.grid(row=xyz, column=2)

        tableLabel = Label(ordersFrame, text=table_no, bg="#202A36", fg="#FFFFFF",
                           font=tkfont.Font(family="Arial Rounded MT Bold", size=16))
        tableLabel.grid(row=xyz, column=4)

        list_pos += 1

    root.mainloop()


def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048)
        message_decoded = message.decode("utf-8")
        message_final = message_decoded.split(",")
        table = message_final[0]
        message_final.pop(0)
        items = []
        qtys = []
        for a in range(0, len(message_final), 2):
            items.append(message_final[a])
        for b in range(1, len(message_final), 2):
            qtys.append(message_final[b])
        kitchenInterface(table, items, qtys)


def communicate_to_server(client):

    threading.Thread(target=listen_for_messages_from_server,
                     args=(client, )).start()


def main_client():
    try:
        client.connect((host, port))
        print("Server Connection Successful")
        usernameDeclaration(client)
    except Exception as e:
        print(f"Unable to connect to server. {host}:{port}\n{e}")


main_client()
listen_for_messages_from_server(client)
