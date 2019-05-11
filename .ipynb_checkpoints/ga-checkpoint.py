import numpy as np
import json
import matplotlib.pyplot as plt


# 适应度函数 f(x)=x+10sin5x+7cos4x
def fitness(x):
    return x + 10 * np.sin(5 * x) + 7 * np.cos(4 * x)


# 个体类
class indivdual:
    def __init__(self):
        self.x = 0  # 染色体编码
        self.fitness = 0  # 适应度值

    def __eq__(self, other):
        self.x = other.x
        self.fitness = other.fitness


# 初始化种群
def initPopulation(pop, N):
    for i in range(N):
        ind = indivdual()
        ind.x = np.random.uniform(-5, 5)  # 均有分布随机
        ind.fitness = fitness(ind.x)  # 计算适应度
        pop.append(ind)


# 选择过程
def selection(N):
    # 种群中随机选择2个个体进行变异（这里没有用轮盘赌，直接用的随机选择）
    return np.random.choice(N, 2)


# 结合/交叉过程
def crossover(parent1, parent2):
    child1, child2 = indivdual(), indivdual()
    child1.x = 0.9 * parent1.x + 0.1 * parent2.x
    child2.x = 0.1 * parent1.x + 0.9 * parent2.x
    child1.fitness = fitness(child1.x)
    child2.fitness = fitness(child2.x)
    return child1, child2


# 变异过程
def mutation(pop):
    # 种群中随机选择一个进行变异
    ind = np.random.choice(pop)
    # 用随机赋值的方式进行变异
    ind.x = np.random.uniform(-5, 5)
    ind.fitness = fitness(ind.x)


# 最终执行
def implement():
    # 种群中个体数量
    N = 20
    # 种群
    POP = []
    # 迭代次数
    iter_N = 500
    # 初始化种群
    initPopulation(POP, N)

    pop_change_list_x = []  # 记录迭代过程
    pop_change_list_y = []  # 记录迭代过程

    # 进化过程
    for it in range(iter_N):
        a, b = selection(N)
        if np.random.random() < 0.75:  # 以0.75的概率进行交叉结合
            child1, child2 = crossover(POP[a], POP[b])
            new = sorted([POP[a], POP[b], child1, child2], key=lambda ind: ind.fitness, reverse=True)  # 根据适应度降序排列
            POP[a], POP[b] = new[0], new[1]
        # 交叉之后再单独计算变异
        if np.random.random() < 0.1:  # 以0.1的概率进行变异
            mutation(POP)

        POP.sort(key=lambda ind: ind.fitness, reverse=True)
        pop_change_list_x.append([i.x for i in POP])
        pop_change_list_y.append([i.fitness for i in POP])

    return POP, pop_change_list_x, pop_change_list_y


pop, pop_change_list_x, pop_change_list_y = implement()

data_x = json.dumps(pop_change_list_x)
data_y = json.dumps(pop_change_list_y)

with open("data_x.json", "w", encoding="utf8") as fp:
    json.dump(data_x, fp)

with open("data_y.json", "w", encoding="utf8") as fp:
    json.dump(data_y, fp)

# 绘图代码

x = np.linspace(-5, 5, 10000)
y = fitness(x)
plt.plot(x, y)
scatter_x = np.array([ind.x for ind in pop])
scatter_y = np.array([ind.fitness for ind in pop])
plt.scatter(scatter_x, scatter_y, c='g')
#
# s_x = x_list[0][0]
# s_y = y_list[0][0]
# plt.scatter(s_x, s_y, c='r')
plt.show()
