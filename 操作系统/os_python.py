import os , threading , socket , start ,time ,datetime ,random , sys ,calendar
from tqdm import trange
from time import sleep
import tkinter as tk
from tkinter import scrolledtext, ttk
import urllib.request
from html.parser import HTMLParser
import re
from multiprocessing import Process, Queue , Lock
from sympy import symbols, Eq, solve, sympify, pretty_print
total_open = start.total_open
total_close = start.total_close
sk = socket.socket()
hostname = start.hostname
addr = start.addr
history = []
history_txt = "history.txt"
random_txt = "random_data.txt"
History = open(history_txt, "a+")
Data = open(random_txt, "a+")
year = start.year
month = start.month
day = start.day
hour = start.hour
minute = start.minute
index = 0
rgb_to_hexstr = lambda rgb: "#" + "".join(map(lambda num: (lambda s: "0" + s if len(s) == 1 else s)(hex(num)[2:]), rgb))
command_list = {"帮助":"help",
     "时间":"time",
     "计算器":"computer",
     "Python控制台":"python",
     "历史记录":"history",
     "清空历史记录":"del history",
     "查看本机Ipv4地址":"ipconfig",
     "分析网页源码":"get url",
     "RGB转十六进制":"RGB -> hex",
     "连接云电脑":"connect cloud computer",
	 "测试概率":"text random"}
class SimpleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href', '')
            self.links.append(href)
            self.text.append(f"[链接: {href}]")
    def handle_data(self, data):
        self.text.append(data)
    def get_parsed_content(self):
        return ''.join(self.text), self.links
class SimpleBrowser:
	def __init__(self, root):
		self.root = root
		self.root.title("简易浏览器")
		self.root.geometry("800x600")
		self.url_frame = ttk.Frame(self.root)
		self.url_frame.pack(fill=tk.X, padx=5, pady=5)
		self.url_entry = ttk.Entry(self.url_frame, width=50)
		self.url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
		self.go_button = ttk.Button(self.url_frame, text="访问", command=self.load_url)
		self.go_button.pack(side=tk.RIGHT)
		self.content_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
		self.content_area.pack(expand=True, fill='both')
		self.url_entry.bind('<Return>', lambda event: self.load_url())
	def load_url(self):
		url = self.url_entry.get().strip()
		if not url:
			return
		if not url.startswith(('http://', 'https://')):
			url = 'http://' + url
		try:
			with urllib.request.urlopen(url) as response:
				content = response.read()
				charset = 'utf-8'
				content_type = response.getheader('Content-Type')
				if content_type:
					match = re.search(r'charset=(\S+)', content_type)
					if match:
						charset = match.group(1)
				try:
					html_content = content.decode(charset)
				except UnicodeDecodeError:
					html_content = content.decode('ISO-8859-1', errors='replace')
				parser = SimpleHTMLParser()
				parser.feed(html_content)
				parsed_text, _ = parser.get_parsed_content()
				self.content_area.delete(1.0, tk.END)
				self.content_area.insert(tk.END, parsed_text)
		except Exception as e:
			self.content_area.delete(1.0, tk.END)
			self.content_area.insert(tk.END, f"错误: {str(e)}")
def simple_calculator():
	expression = input("\033[34mInput math>>>\033[0m").strip()
	if not expression:
		print("\033[31mInput errors\033[0m")
		return
	try:
		allowed_chars = set('0123456789+-*/.()')
		if not all(c in allowed_chars for c in expression):
			raise ValueError("\033[31mInput errors\033[0m")
		result = eval(expression)
		print(f"result: {result}")
	except ZeroDivisionError:
		print("\033[31mInput errors\033[0m")
	except SyntaxError:
		print("\033[31mInput errors\033[0m")
	except ValueError as e:
		print(f"错误：{e}")
	except Exception:
		print("\033[31mTake a errors\033[0m")
def random_probability(probability,min=0,max=100):
	random_number = random.uniform(min,max)
	if random_number <= probability:
		return True
	else:
		return False
def solve_math():
    while True:
        print("\n===== 方程求解器 =====")
        print("1. 一元一次方程")
        print("2. 二元一次方程组")
        print("3. 三元一次方程组")
        print("4. 一元二次方程")
        print("5. 退出")
        choice = input("请输入选项编号（1-5）：").strip()

        if choice == '5':
            print("感谢使用，再见！")
            break

        try:
            if choice == '1':
                # 一元一次方程
                eq_str = input("请输入一元一次方程（例如：3*x + 5 = 0）：")
                x = symbols('x')
                lhs, rhs = map(sympify, eq_str.split('='))
                eq = Eq(lhs, rhs)
                solution = solve(eq, x)
                if not solution:
                    print("该方程无解。")
                else:
                    pretty_print(f"解为：{solution[0]}")
                    print(f"近似值：{solution[0].evalf()}")

            elif choice == '2':
                # 二元一次方程组
                print("请输入两个方程，每个方程以等号结尾，例如：2*x + y = 8")
                eq1_str = input("第一个方程：")
                eq2_str = input("第二个方程：")
                x, y = symbols('x y')
                lhs1, rhs1 = map(sympify, eq1_str.split('='))
                lhs2, rhs2 = map(sympify, eq2_str.split('='))
                eq1 = Eq(lhs1, rhs1)
                eq2 = Eq(lhs2, rhs2)
                solutions = solve((eq1, eq2), (x, y))
                if not solutions:
                    print("方程组无解。")
                else:
                    pretty_print("解为：")
                    for var, val in zip([x, y], solutions):
                        print(f"{var} = {val}")
                    print("近似值：")
                    for var, val in zip(['x', 'y'], [v.evalf() for v in solutions]):
                        print(f"{var} ≈ {val}")

            elif choice == '3':
                # 三元一次方程组
                print("请输入三个方程，每个方程以等号结尾，例如：x + y + z = 6")
                eq1_str = input("第一个方程：")
                eq2_str = input("第二个方程：")
                eq3_str = input("第三个方程：")
                x, y, z = symbols('x y z')
                lhs1, rhs1 = map(sympify, eq1_str.split('='))
                lhs2, rhs2 = map(sympify, eq2_str.split('='))
                lhs3, rhs3 = map(sympify, eq3_str.split('='))
                eq1 = Eq(lhs1, rhs1)
                eq2 = Eq(lhs2, rhs2)
                eq3 = Eq(lhs3, rhs3)
                solutions = solve((eq1, eq2, eq3), (x, y, z))
                if not solutions:
                    print("方程组无解。")
                    pretty_print("解为：")
                    for var, val in zip([x, y, z], solutions):
                        print(f"{var} = {val}")
                    print("近似值：")
                    for var, val in zip(['x', 'y', 'z'], [v.evalf() for v in solutions]):
                        print(f"{var} ≈ {val}")

            elif choice == '4':
                # 一元二次方程
                eq_str = input("请输入一元二次方程（例如：x**2 - 5*x + 6 = 0）：")
                x = symbols('x')
                lhs, rhs = map(sympify, eq_str.split('='))
                eq = Eq(lhs, rhs)
                solutions = solve(eq, x)
                if not solutions:
                    print("该方程无实数解。")
                else:
                    pretty_print("解为：")
                    for sol in solutions:
                        print(f"x = {sol}")
                    print("近似值：")
                    for sol in solutions:
                        print(f"x ≈ {sol.evalf()}")

            else:
                print("无效的选项，请重新输入。")

        except Exception as e:
            print(f"发生错误：{e}")
            print("请检查输入的方程格式是否正确。")
for i in trange(total_open):
	for j in range(total_open):
		k = i* j
History.write(f"\n{hostname}  {year} {month} {day}  {hour}:{minute}")
print("\033[33mWelcome\033[0m")

try:
	while True:
		command = input("\033[32m>>>\033[0m")
		index += 1
		history_things = f"{index}.{command}"
		history.append(history_things)
		History.write(f"\n{history_things}")
		if command == "exit" or command=="退出" or command=="quit":
			for i in trange(total_close):
				for j in range(total_close):
					k = i * j
			History.close()
			Data.close()
			print('\033[33mGoodbye\033[0m')
			sleep(2)
			break
		elif command=="time" or command=="时间":
			print(datetime.datetime.now())
		elif command=="computer" or command=="计算器":
			simple_calculator()
		elif command=="python" or command=="Python" or command=="控制台":
			while True:
				try:
					cmd = input("\033[34m>>>\033[0m")
					if cmd.lower() in ('exit','quit','退出'):
						break
					exec(cmd)
				except KeyboardInterrupt:
					print("\nUse 'exit' or 'quit' to exit")
				except Exception as e:
					print(f"\033[31mError: {e}\033[0m")
		elif command == "history" or command == "历史记录":
			for a in history:
				print(a)
		elif command == "del history" or command == "清空历史记录":
			print("Would you like to remove history?(True/false)")
			del_history_agree = input("\033[34m>>>\033[0m")
			if del_history_agree == "True" or del_history_agree == "true" or del_history_agree == "yes" or del_history_agree == "Yes" or del_history_agree ==  "y" or del_history_agree == "Y":
				index = 0
				history.clear()
				print("del history successfully")
		elif command == "ipconfig" or command == "查看本机Ipv4地址":
			print(addr)
		elif command == "get url" or command == "分析网页源码" or command == "分析网页源代码":
			root = tk.Tk()
			browser = SimpleBrowser(root)
			root.mainloop()
		elif command == "RGB -> hex":
			print(rgb_to_hexstr(map(int, input("\033[34m>>>\033[0m").split(","))))
		elif command == "connect cloud computer":
			try:
				print("input your ip_address")
				address = input("\033[34m>>>\033[0m")
				print("input your port")
				port = int(input("\033[34m>>>\033[0m"))
				print("connecting",end="",flush=True)
				for i in range(5):
					print(".", end="", flush=True)
					sleep(1)
				print("")
				sk.connect((address, port))
				while True:
					command_socket = input("\033[34m>>>\033[0m")
					sk.send(command_socket.encode("utf-8"))
					if command_socket=="exit":
						break
					data = sk.recv(1024)
					print(data.decode("utf-8"))
			except:
				print("\033[31mAn error occurred during inputting command\033[0m")
				History.write("\nAn error occurred during inputting command")
				History.close()
				Data.close()
				for i in trange(total_close):
					for j in range(total_close):
						k = i * j
				print('\033[33mGoodbye\033[0m')
				sleep(2)
				break
		elif command == "help":
			for i, j in command_list.items():
				print(i, j)
		elif command == "text random":
			Data.write(f"\n{hostname}  {year} {month} {day}  {hour}:{minute}")
			while True:
				print("Input a probability")
				probability = input("\033[34m>>>\033[0m")
				if probability == "exit" or probability=="quit":
					break
				probability = float(probability)
				event_take_place = random_probability(probability)
				Data.write(f"\n{str(event_take_place)}")
				print(event_take_place)
		elif command == "solve math":
			solve_math()
		elif command == "calendar-now":
			print(f"\033[35m{calendar.month(year,month)}\033[0m")
			month = start.month
		elif command == "calendar-last":
			month -= 1
			print(f"\033[35m{calendar.month(year,month)}\033[0m")
			month = start.month
		elif command == "calendar-tomorrow":
			month += 1
			print(f"\033[35m{calendar.month(year,month)}\033[0m")
			month = start.month
		elif command == "":
			continue
		else:
			print("\033[31mInput errors\033[0m")
except:
	print("\033[31mAn error occurred during inputting command\033[0m")
	History.write("\nAn error occurred during inputting command")
	History.close()
	Data.close()
	for i in trange(total_close):
		for j in range(total_close):
			k = i * j
	print('\033[33mGoodbye\033[0m')
	sleep(2)