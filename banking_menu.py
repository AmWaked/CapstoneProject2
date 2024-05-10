import tkinter
import csv


class BankMenu(tkinter.Tk):
    """
    main window for banking app
    """
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('Wakefield Bank')
        self.geometry('300x400')
        self.resizable(False, False)

        self.container = tkinter.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.current_user = None
        self.username = 'x'
        self.password = 'y'
        self.balance = 0

        self.frames = {}
        for F in (WelcomePage, LoginPage, MainMenu, GetBalance, Deposit, Withdraw):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('WelcomePage')

    def show_frame(self, page_name) -> None:
        frame = self.frames[page_name]
        frame.tkraise()


class WelcomePage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        self.welcome_label = tkinter.Label(self, text='Welcome to Wakefield Bank', font=('Arial', 14))
        self.welcome_label.pack(pady=10)
        self.login_button = tkinter.Button(self, text='Log In', command=lambda: self.controller.show_frame('LoginPage'))
        self.login_button.pack()
        self.exit_button = tkinter.Button(self, text='Exit', command=quit)
        self.exit_button.pack()


class LoginPage(tkinter.Frame):
    """

    Frame for verifying and setting up to record voter ID

    """

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.username_label = tkinter.Label(self, text='Input your username:')
        self.username_label.pack(side='top', fill='x', pady=10)
        self.input_username = tkinter.Entry(self, width=20)
        self.input_username.pack()
        self.password_label = tkinter.Label(self, text='Input your password:')
        self.password_label.pack(side='top', fill='x', pady=10)
        self.input_password = tkinter.Entry(self, width=20, show='*')
        self.input_password.pack()
        self.submit_button = tkinter.Button(self, text='Submit', command=self.login)
        self.submit_button.pack()
        self.restart_button = tkinter.Button(self, text='Return', command=self.restart)
        self.restart_button.pack()

    def login(self) -> None:
        """

        checks validity of bank account from csv

        """
        try:
            self.controller.username = (self.input_username.get())
            self.controller.password = (self.input_password.get())
            is_valid = self.login_validity(self.controller.username, self.controller.password)
            if is_valid:
                self.controller.current_user = self.controller.username
                self.controller.show_frame('MainMenu')
            else:
                self.login_exceptions('Invalid username or password')

        except ValueError:
            self.login_exceptions('Invalid username or password')

    def login_validity(self, username, password) -> bool:
        """
        Reads the CSV file and checks if the username and password are valid
        """
        try:
            with open('accounts.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['username'] == username and row['password'] == password:
                        return True
        except FileNotFoundError:
            self.login_exceptions('Login failed')
            return False

    def login_exceptions(self, message) -> None:
        """

        shows problem text for user

        """
        self.username_label.config(text=message, fg='red', font=('16'))
        self.username_label.pack(side='top', fill='x', pady=10)

    def restart(self) -> None:
        """

        returns user to start and resets input fields

        """
        self.input_username.delete(0, 'end')
        self.input_password.delete(0, 'end')
        self.controller.show_frame('WelcomePage')


class MainMenu(tkinter.Frame):
    """
    frame for displaying bank options
    """
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        self.check_balance_button = tkinter.Button(self, text='Check Balance',
                                                   command=lambda: self.controller.show_frame('GetBalance'))
        self.check_balance_button.pack(pady=(20, 10))

        self.deposit_button = tkinter.Button(self, text='Deposit',
                                             command=lambda: self.controller.show_frame('Deposit'))
        self.deposit_button.pack(pady=10)

        self.withdraw_button = tkinter.Button(self, text='Withdraw',
                                              command=lambda: self.controller.show_frame('Withdraw'))
        self.withdraw_button.pack(pady=10)


class GetBalance(tkinter.Frame):
    """
    frame for showing current account balance
    """
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.balance_label = None
        self.controller = controller
        label = tkinter.Label(self, text='Balance', font=18)
        label.pack(pady=10)
        self.balance = self.get_current_balance()

        self.get_balance = tkinter.Button(self, text='Get Balance',
                                          command=self.get_current_balance())
        self.get_balance.pack()

        back_button = tkinter.Button(self, text='Back to Main Menu',
                                     command=lambda: self.controller.show_frame('MainMenu'))
        back_button.pack()

    def get_current_balance(self) -> None:
        """
        access csv to see account balance
        """
        self.balance_label = tkinter.Label(self, text=f'Balance - ${self.controller.balance}')
        self.balance_label.pack()
        with (open('accounts.csv', newline='') as csvfile):
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == self.controller.username:
                    self.balance = row['balance']
                    return self.balance


class Deposit(tkinter.Frame):
    """
    frame for depositing into account
    """
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        label = tkinter.Label(self, text='Deposit', font=18)
        label.pack(pady=10)

        self.deposit_label = tkinter.Label(self, text='How much would you like to deposit?')
        self.deposit_label.pack(side='top', fill='x', pady=10)
        self.input_deposit = tkinter.Entry(self, width=20)
        self.input_deposit.pack()
        self.submit_deposit = tkinter.Button(self, text='Submit',
                                             command=self.deposit)
        self.submit_deposit.pack()

        back_button = tkinter.Button(self, text='Back to Main Menu',
                                     command=lambda: self.controller.show_frame('MainMenu'))
        back_button.pack()

    def deposit(self) -> None:
        """
        access csv to get current balance then add deposit amount
        """

        with (open('accounts.csv', newline='') as csvfile):
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == self.controller.username:
                    self.balance = (row['balance'])
                    return float(self.balance)
        self.deposit_amt = (self.input_deposit.get())
        self.controller.balance = self.deposit_amt + self.controller.balance


class Withdraw(tkinter.Frame):
    """
    frame for withdrawing from account
    """
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        label = tkinter.Label(self, text='Withdraw', font=18)
        label.pack(pady=10)

        self.withdraw_label = tkinter.Label(self, text='How much would you like to withdraw?')
        self.withdraw_label.pack(side='top', fill='x', pady=10)
        self.input_withdraw = tkinter.Entry(self, width=20)
        self.input_withdraw.pack()
        self.submit_withdraw = tkinter.Button(self, text='Submit',
                                              command=self.withdraw)
        self.submit_withdraw.pack()
        self.back_button = tkinter.Button(self, text='Back to Main Menu',
                                          command=lambda: self.controller.show_frame('MainMenu'))
        self.back_button.pack()

    def withdraw(self) -> None:
        """
        access csv file for balance then subtract withdraw amount
        """
        with (open('accounts.csv', newline='') as csvfile):
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'].strip() == self.controller.username.strip():
                    self.balance = (row['balance'])
                    return float(self.balance)
        self.withdraw_amt = (self.input_withdraw.get())
        self.controller.balance = self.controller.balance - self.withdraw_amt


BankMenu().mainloop()
