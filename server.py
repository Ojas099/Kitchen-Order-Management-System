import traceback
import socket
import threading

host = 'xxx.xxx.xxx.xxx'  # The IPv4 address of the server hosting computer
port = 9999  # Data type should be int
active_clients = []

dish_styles = {
    "Pav Bhaji": "North Indian",
    "Mint Mojito": "Beverages",
    "Masala Dosa": "South Indian",
    "Chhole Bhature": "North Indian",
    "White Sauce Pasta": "Western"
}


def listen_for_messages(client):
    while 1:
        try:
            message_rcvd = client.recv(2048)
            message_rcvd_decoded = message_rcvd.decode('utf-8')
            if message_rcvd_decoded == "":
                continue
            message_rcvd_final = message_rcvd_decoded.split(',')
            print(len(message_rcvd_final))
            username = message_rcvd_final[0]
            message_type = message_rcvd_final[1].lower()
            message_rcvd_final.pop(1)
            message_rcvd_final.pop(0)

            if message_type == "order msg":
                only_items = []
                only_qtys = []
                only_styles = []
                for i in range(0, len(message_rcvd_final), 2):
                    only_items.append(message_rcvd_final[i])
                for j in range(1, len(message_rcvd_final), 2):
                    only_qtys.append(message_rcvd_final[j])
                for k in only_items:
                    only_styles.append(dish_styles[k])
                active_clients.append(username)
                active_clients.append(client)
                send_messages_to_all(username, only_items,
                                     only_qtys, only_styles)
            elif message_type == "username declaration":
                active_clients.append(username)
                active_clients.append(client)

        except Exception:
            traceback.print_exc()
            break


def send_message_to_client(target, message):
    final_message = ','.join(message)
    for abcd in active_clients:
        if abcd == target:
            index = int(active_clients.index(abcd))
            kitchen_socket = active_clients[index+1]
            kitchen_socket.sendall(final_message.encode('utf-8'))


def send_messages_to_all(username, items, qtys, styles):
    for x in range(len(items)):
        msg = [username]
        msg.append(items[x])
        msg.append(qtys[x])
        target = styles[x]
        send_message_to_client(target, msg)
        msg.clear()


def main():
    print(f"Server started at {host} {port}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((host, port))
    except:
        print(f"Sorry, Network Error! Try Again")
    server.listen(5)
    while 1:
        client, address = server.accept()
        print(f"New Client connected at {address}")

        threading.Thread(target=listen_for_messages, args=(client, )).start()


main()
