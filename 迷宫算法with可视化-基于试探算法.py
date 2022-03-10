
# 迷宫规定：只能走其上下左右四个方向点
# 使用笛卡尔坐标系
import copy

class Maze:
    def __init__(self, maze_list, starting_point, end_point):
        self.maze_list = maze_list  # 迷宫列表
        self.start_point = starting_point   # 起点
        self.end_point = end_point      # 终点
        self.w, self.h = len(self.maze_list[0]), len(self.maze_list)        # 迷宫长、宽
        self.is_arrival = False     # 判断是否到达
        self.current_point = starting_point     # 当前点
        self.motion_path = [self.start_point]   # 单个解
        self.all_path = []      # 全部解

    # 可行点
    def feasible_point(self, point):
        self.tem_list = copy.deepcopy(self.maze_list)
        for i in self.motion_path:
            self.tem_list[i[1]][i[0]] = 2
        x, y = point
        sur_point = [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]
        real_point = []
        for i in sur_point:
            if i[0] < 0 or i[1] < 0:
                continue
            if i[0] >= self.w or i[1] >= self.h:
                continue
            real_point.append(i)
        fea_list = []
        for i in real_point:
            if not self.tem_list[i[1]][i[0]]:
                fea_list.append(i)
        if fea_list == []:
            return None
        return fea_list

    def display_maze(self, motion_path=None):
        if motion_path is None:
            motion_path = self.motion_path[:]
        self.tem_list = copy.deepcopy(self.maze_list)
        for i in motion_path:
            self.tem_list[i[1]][i[0]] = 2
        return self.tem_list

    def default(self, width, w_h=(1080, 720), index=0):
        self.result_display(self.maze_list, self.get_best_path(index=index), width, w_h=w_h)
        # self.result_display(self.maze_list, self.paint_all_feasible_path(), width, w_h=w_h)

    def conflict(self, point):
        # 死路点不可取
        if self.feasible_point(point) is None:
            return True
        return False

    def perm(self, point):
        if self.current_point == self.end_point:
            self.is_arrival = True

        if self.is_arrival:
            # 到达终点

            print(self.display_maze())
            self.all_path.append(self.motion_path[:])
        else:
            for i in point:
                self.motion_path.append(i)
                self.current_point = i
                if self.feasible_point(i) is None and i == self.end_point:
                    self.all_path.append(self.motion_path[:])
                if not self.conflict(i):
                    self.perm(self.feasible_point(i))
                self.motion_path.pop()      # 剪枝

    def get_all_path_maze(self):
        for i in self.all_path:
            print(i)
            print(self.display_maze(i))
            print("\n")

    def get_best_path(self, index=0):
        count_path = [(i, j) for i, j in zip(self.all_path, [len(k) for k in self.all_path])]
        count_path.sort(key=lambda y: y[1])
        print([i[1] for i in count_path])
        return count_path[index][0]

    def paint_all_feasible_path(self):
        all_set = set()
        for i in self.all_path:
            for j in i:
                all_set.add(j)
        return list(all_set)

    def get_sorted_path(self):
        count_path = [(i, j) for i, j in zip(self.all_path, [len(k) for k in self.all_path])]
        count_path.sort(key=lambda y: y[1])
        return [i[0] for i in count_path]

    def result_display(self, maze_list, motion_path, width, font=("微软雅黑", 13), w_h=(1080, 720)):
        import tkinter
        import tkinter.messagebox
        from project.CaDt.window_center import set_win_center
        self.window = tkinter.Tk()
        self.window.resizable(False, False)
        self.window["bg"] = "white"
        self.window.update()
        set_win_center(self.window, *w_h)

        from project.CaDt.binary_data import program_ico
        from io import BytesIO
        from PIL import Image, ImageTk
        self.window.iconphoto(True, ImageTk.PhotoImage(Image.open(BytesIO(program_ico()))))
        self.window.title(f'迷宫算法')

        self.Label_Frame = tkinter.LabelFrame(bg="white")
        self.Label_Frame.pack(expand=1)
        Label_list = []
        font_list = []
        for i in range(len(maze_list)):
            Label_list.append([])
            font_list.append([])
            for j in range(len(maze_list[0])):
                Label_list[i].append(
                    tkinter.Canvas(self.Label_Frame, width=width, height=width, bd=0, bg="#05bbfb", relief="flat",
                                   cursor="hand2"))
                Label_list[i][j].grid(row=i, column=j, padx=0, pady=0)

        def paint():
            color_dict = {1: "#05bbfb", 0: "#c6c6c6", 2: "#ff678a"}
            for y in range(len(maze_list)):
                for x in range(len(maze_list[0])):
                    Label_list[y][x].config(bg=color_dict[maze_list[y][x]])
            Label_list[self.start_point[1]][self.start_point[0]].create_text(width / 2 + 1, width / 2 + 1, text="起点",
                                                                             font=font)
            Label_list[self.end_point[1]][self.end_point[0]].create_text(width / 2 + 1, width / 2 + 1, text="终点",
                                                                         font=font)

        import time
        def path_display(k=0):
            Label_list[motion_path[k][1]][motion_path[k][0]].config(bg="#ff678a")
            if k < len(motion_path)-1:
                self.window.after(200, lambda: path_display(k+1))

        self.window.after(1000, path_display)
        paint()


        self.window.mainloop()

    @staticmethod
    def set_maze(width, w_h=(7, 7), canvas=(1080, 720)):
        import tkinter
        import tkinter.messagebox
        from project.CaDt.window_center import set_win_center
        window = tkinter.Tk()
        window.resizable(False, False)
        window["bg"] = "white"
        window.update()
        set_win_center(window, *canvas)

        mz_list = [[1 for _ in range(w_h[0])] for _ in range(w_h[1])]

        from project.CaDt.binary_data import program_ico
        from io import BytesIO
        from PIL import Image, ImageTk
        window.iconphoto(True, ImageTk.PhotoImage(Image.open(BytesIO(program_ico()))))
        window.title(f'迷宫算法')

        Label_Frame = tkinter.LabelFrame(bg="white")
        Label_Frame.pack(expand=1)
        Label_list = []
        font_list = []
        for i in range(w_h[1]):
            Label_list.append([])
            font_list.append([])
            for j in range(w_h[0]):
                Label_list[i].append(
                    tkinter.Canvas(Label_Frame, width=width, height=width, bd=0, bg="#05bbfb", relief="flat",
                                   cursor="hand2"))
                Label_list[i][j].grid(row=i, column=j, padx=0, pady=0)

        x = [0]
        y = [0]

        def set_color(i, j):

            if mz_list[i][j]:
                mz_list[i][j] = 0
                Label_list[i][j].config(bg="#c6c6c6")
            else:
                mz_list[i][j] = 1
                Label_list[i][j].config(bg="#05bbfb")

            print("\n=========================================")
            print(mz_list)



        # i 是 y， j是x
        def add_command(i=0, j=0):
            x[0], y[0] = i, j
            Label_list[i][j].bind("<Button-1>", lambda event: set_color(i, j))

            if i < len(Label_list) - 1:
                if j < len(Label_list[0]) - 1:
                    add_command(i, j + 1)
                if j == len(Label_list[0]) - 1:
                    add_command(i + 1, 0)
            elif i == len(Label_list) - 1:
                if j < len(Label_list[0]) - 1:
                    add_command(i, j + 1)



        def add_total():
            try:
                add_command(i=x[0], j=y[0])
            except:
                add_total()

        add_total()




        window.mainloop()


mz_list = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
           [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
           [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
           [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
           [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]]

mz = Maze(maze_list=mz_list, starting_point=(0, 10), end_point=(37, 19))
mz.perm([(0, 10)])
mz.default(30, (1480, 720), 0)
# mz = Maze.set_maze(30, w_h=(40, 20), canvas=(1480, 720))








