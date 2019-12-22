# 滑模控制
这个库主要用于介绍滑模控制的相关概念。

## 一维运动模型

考虑简单的单位质量块的一维运动模型，使用位移和速度状态变量进行描述。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191220200846.png)

如下图所示，是无外界干扰项时的渐近收敛效果图，图中蓝色线代表距离，橘黄色线代表速度。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191220194837.png#pic_center)

加入外部干扰，响应波形如下：

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191220194841.png#pic_center)

## 滑模控制的主要特性

下图表示，在有限的时间内，滑模变量趋近于0。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191221143643.png)

在干扰项作用的情况下，状态变量逐渐收敛到0。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191221143647.png)

相图如下，展示了到达相位和滑移相位。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191221143650.png)

对上面的相图进行局部放大发现，在滑模状态下，状态变量存在小幅度且高频率的蜿蜒运动。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191221144252.png)

理想的滑模切换频率应该接近于无限并且蜿蜒运动的振幅接近于0。

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/Figure_7.png)

![](https://raw.githubusercontent.com/zgh551/FigureBed/master/img/20191222084921.png)

