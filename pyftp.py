import tkinter as tk
from tkinter import messagebox
from ftplib import FTP

class FTPClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FTP Client")

        # Server entry
        self.server_label = tk.Label(root, text="Server:")
        self.server_label.grid(row=0, column=0)
        self.server_entry = tk.Entry(root)
        self.server_entry.grid(row=0, column=1)

        # Username entry
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=1, column=0)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=1, column=1)

        # Password entry
        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=2, column=1)

        # Connect button
        self.connect_button = tk.Button(root, text="Connect", command=self.connect)
        self.connect_button.grid(row=3, column=0, columnspan=2)

        # Command entry
        self.command_label = tk.Label(root, text="Command:")
        self.command_label.grid(row=4, column=0)
        self.command_entry = tk.Entry(root)
        self.command_entry.grid(row=4, column=1)

        # Execute button
        self.execute_button = tk.Button(root, text="Execute", command=self.execute_command)
        self.execute_button.grid(row=5, column=0, columnspan=2)

        # Text area for displaying messages
        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.grid(row=6, column=0, columnspan=2)

        # FTP instance
        self.ftp = None

    def connect(self):
        server = self.server_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not server:
            messagebox.showerror("Error", "Please enter the server address.")
            return

        if not username:
            username = "anonymous"

        try:
            self.ftp = FTP(server)
            self.ftp.login(user=username, passwd=password)
            self.text_area.insert(tk.END, f"Connected to {server} as {username}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")

    def execute_command(self):
        if not self.ftp:
            messagebox.showerror("Error", "Please connect to the server first.")
            return

        command = self.command_entry.get().strip()
        if not command:
            messagebox.showerror("Error", "Please enter a command.")
            return

        try:
            if command.lower() == "ls":
                files = self.ftp.nlst()
                self.text_area.insert(tk.END, "Files in current directory:\n")
                for file in files:
                    self.text_area.insert(tk.END, f"{file}\n")
            elif command.lower().startswith("get "):
                filename = command.split(" ")[1]
                with open(filename, "wb") as file:
                    self.ftp.retrbinary(f"RETR {filename}", file.write)
                self.text_area.insert(tk.END, f"{filename} downloaded successfully.\n")
            elif command.lower().startswith("put "):
                filename = command.split(" ")[1]
                with open(filename, "rb") as file:
                    self.ftp.storbinary(f"STOR {filename}", file)
                self.text_area.insert(tk.END, f"{filename} uploaded successfully.\n")
            elif command.lower().startswith("cd "):
                directory = command.split(" ")[1]
                self.ftp.cwd(directory)
                self.text_area.insert(tk.END, f"Changed directory to {directory}\n")
            elif command.lower() == "quit":
                self.ftp.quit()
                self.text_area.insert(tk.END, "Disconnected from server\n")
            else:
                self.text_area.insert(tk.END, "Invalid command. Available commands: ls, get, put, cd, quit\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute command: {str(e)}")

def main():
    root = tk.Tk()
    ftp_client_gui = FTPClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

