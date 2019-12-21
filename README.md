# 滑模控制
这个库主要用于介绍滑模控制的相关概念。

# # 一维运动模型

考虑简单的单位质量块的一维运动模型，使用位移和速度状态变量进行描述。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191220200846.png)

定义位移变量$x$和速度变量$v = \dot{x}$，运动模型的微分形式如下：
$$
\left\{
\begin{array}{rl}
&dx = \dot{x}& x(0)=x_0\\
&d\dot{x} = u + f(x,\dot{x},t) &\dot{x}(0)=\dot{x}_0
\end{array} \right.\tag{1}
$$



其中,$u$代表控制力，干扰项$f(x,\dot{x},t)$包括干粘摩檫力的影响和一些未知的阻力，并假定有界。
$$
\rvert f(x,\dot{x},t)\rvert \leqslant L \gt 0 \tag{2}
$$
问题关键在于设计一个反馈控制率$u = u(x,\dot{x})$，驱动质量块渐进到达原点。换句话说，控制变量$u=f(x,\dot{}x)$应该驱使状态变量为0：$\lim_{t \rightarrow \infty}{x,\dot{x}} = 0$。

这个看似简单的问题，对于存在未知的边界干扰项$f(x,\dot{x},t)$的情况下，实现渐进收敛存在着挑战。



例如，通过一个线性状态反馈控制率
$$
\begin{matrix}
u = -k_1x - k_2\dot{x}, &\text{其中}(k_1>0,&k_2>0)
\end{matrix}\tag{3}
$$
在外界干扰项$f(x,\dot{x},t)\equiv0$时，系统可以实现渐进收敛。

给定初始条件$x_0=1$、$\dot{x} = -2$、控制率参数$k_1=3$、$k_2=4$。

如下图所示，是无外界干扰项时的渐近收敛效果图，图中蓝色线代表距离，橘黄色线代表速度，可以看出在反馈控制率$u = u(x,\dot{x})$的作用下，距离和速度值都趋近于0。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191220194837.png#pic_center)

加入外部干扰$f(x,\dot{x},t) = \sin(2t)$，响应波形如下：

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191220194841.png#pic_center)


$$

$$

产生的边界范围为$\Omega=(k_1,k_2,L)$。

## 滑模控制的主要特性

下图表示，在有限的时间内，滑模变量趋近于0。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191221143643.png)

在干扰项作用的情况下，状态变量$x$和$\dot{x}$逐渐收敛到0。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191221143647.png)

相图如下，展示了到达相位和滑移相位。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191221143650.png)

对上面的相图进行局部放大发现，在滑模状态下，状态变量存在小幅度且高频率的蜿蜒运动。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191221144252.png)

理想的滑模切换频率应该接近于无限并且蜿蜒运动的振幅接近于0。

