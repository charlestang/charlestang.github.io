---
title: Linux 系统资源管理：什么是 CGroups ？
tags:
  - Linux
id: '821'
categories:
  - - 技术
    - 运维
permalink: whats-cgroups/
date: 2019-06-11 00:20:50
---

## 综述

CGroups 是 **Control Groups** 的缩写，是 Linux 内核的一种机制，可以**分配**、**限制**和**监控**一组任务（进程）使用的物理资源（CPU、内存、磁盘I/O、带宽或这几种资源的组合）。

这里有几个基本概念需要知道：

*   **任务（Task）**—— 一个系统进程在这个机制的语境下，称为一个任务。
*   **控制组（Control Group）**—— 控制组就是一组按照某种规则分组的进程，并且关联了一组参数或者限制。控制组是层次结构化的，一个控制组可以从自己的父节点继承属性。
*   **子系统（Subsystem）**—— 也叫做资源控制器，或者控制器。是一种单一资源的抽象，比如 CPU 时间，或者内存等。
*   **层次结构（Hirerarchy）**—— 一种层次化的结构，可以用来附着（attach）一些子系统。因为控制组是层次结构化的，它们所形成的一棵树称作一个层次结构。

CGroups 提供了一个虚拟文件系统 /proc/cgroup，作为交互的接口，用于设置和管理各个子系统。本质上来说，CGroups 是内核附加在程序上的一系列钩子（Hooks），通过程序运行时对资源的调度触发相应的钩子以达到资源追踪和限制的目的。[7]

![](../images/2019/06/cgroups-timeline.png)

CGroups 发展的时间线

### 核心特性

*   **资源限制** —— 一组进程不可超过内存的使用限制，包括文件系统的 Cache
*   **优先级** —— 一组进程相对可以获得较大的 CPU 时间和 I/O 占用
*   **审计** —— 衡量一组任务的资源利用，比如，这种数据可以用来计费
*   **控制** —— 冻结或者恢复一组进程

### 几个概念间的关系

![](../images/2019/06/RMG-rule1.png)

一个层次结构，可以附着一个或者多个子系统（来源 RedHat）

![](../images/2019/06/RMG-rule2.png)

一个子系统不能附着第二个已经附着过子系统的层次结构

![](../images/2019/06/RMG-rule3.png)

一个任务不能是同一个层次结构下的不同控制组的成员

![](../images/2019/06/RMG-rule4.png)

fork 出来的进程严格继承父进程的控制组

## CGroups 的基本使用

在实践中，系统管理员会用 CGroups 干类似这些事情[8]：

*   隔离一个进程集合（比如：nginx的所有进程），并限制他们所消费的资源，比如绑定CPU的核。
*   为这组进程 分配其足够使用的内存
*   为这组进程分配相应的网络带宽和磁盘存储限制
*   限制访问某些设备（通过设置设备的白名单）

因为是一个 /proc 目录下的伪文件系统，我们总是可以用 Shell 的命令来操作和管理 CGroups，但是更简单的办法是安装一个 libcgroup 的包[6]，它提供了好几个命令行工具和相关的文档。这个包里面提供一个 cgconfig 的服务，以及 /etc/cgconfig.conf 配置文件的通过系统运维脚本 service 就可以有效实现层次结构的创建和子系统的附着，以及参数设置等工作，非常方便。具体可以参阅 RHEL 6 的指南。

## CGroups 的实现方式

![](../images/2019/06/cgroups-source-graph-1024x686.png)

Linux 内核中关于 CGroups 的源码结构示意图[7]

上面是一幅 Linux 内核源码中，跟 CGroups 有关的数据结构的关系图。task_struct 结构体就是描述进程的数据结构，里面通过一个指针 cgoups 关联到一个辅助的数据结构叫 css_set，css_set 又通过一个辅助的数据结构叫 cg_cgroup_link 关联到 cgroup，至此完成了进程和 cgroup 的映射。因为一个进程可以属于多个 cgroup（必须分属不同的 Hirerarchy），一个 cgroup 也可以关联多个进程，所以，cg_cgroup_link 就是一个处理多对多关系的“表”。

cgroup 里面有 sibling，children，parent 指针，显示 cgroup 结构体，本质上是一个“树”的节点（node）数据结构。所以，cgroup 是树形的结构。有一个 root 指针，指向了树的根 cgroupfs_root。树根，其实就是我们说的“层次结构”（Hirerarchy）。

cgroup_subsys 就是我们说的“子系统”的数据结构。这是一个抽象数据结构，需要被各个子系统去分别实现，所以这里包含了很多函数指针（如 attach）。cgroup_subsys_state 存储了一些各个子系统共用的元数据。各个子系统各自的结构体，按照自己的特点再来定义各自的控制信息结构体。参考[7]

![](../images/2019/06/cgroups-logic-graph-984x1024.png)

从逻辑层面看 CGroups 的内核数据结构[10]

上图引自美团技术博客的一篇文章，从逻辑结构层面，描述了进程、子系统、群组和层次结构的关系。见参考文献[10]。

## 结语

CGroups 是内核提供的操作系统层面的虚拟化关键技术。是 Docker 这类杀手级应用的理论基础。本文只是对作者学习此概念时候看到的一系列文章的内容进行了编纂和综述，尝试从一个门外汉的角度去对该项技术形成一定的理解。如需细致学习，还请以参考文献中的文章内容为标准。

通过研究和学习这些资料，总结出一个基本判断就是，Linux 内核提供了比较完备的虚拟化技术，即使没有 Docker 这样的系统化的应用技术，我们也可以实现对一些机器资源的灵活管理。内核本来就提供了这样的工具。通过学习完全是可以掌握的。但是，Docker 这类技术，则提供了更为友好，高效的操作接口，极大提升了工程效率，降低了学习难度，更值得在生产中推广。

参考文献：

1.  [https://lwn.net/Articles/199643/](https://lwn.net/Articles/199643/) Rohit Setch 提交 patch
2.  [https://lwn.net/Articles/236038/](https://lwn.net/Articles/236038/) Paul Menage 接手容器的开发
3.  [https://en.wikipedia.org/wiki/Cgroups](https://en.wikipedia.org/wiki/Cgroups) Wiki：cgroups
4.  [https://www.kernel.org/doc/Documentation/cgroup-v1/cgroups.txt](https://www.kernel.org/doc/Documentation/cgroup-v1/cgroups.txt)
5.  [https://www.kernel.org/doc/Documentation/cgroup-v2.txt](https://www.kernel.org/doc/Documentation/cgroup-v2.txt)
6.  [RHEL 6 资源管理指南](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html-single/resource_management_guide/index#idm140126110528416)
7.  [Docker背后的内核知识——CGroups资源限制](https://www.infoq.cn/article/docker-kernel-knowledge-cgroups-resource-isolation/)
8.  [Docker基础技术——Linux CGroups](https://coolshell.cn/articles/17049.html)
9.  [CGroup 的介绍、应用实例和原理描述](https://www.ibm.com/developerworks/cn/linux/1506_cgroup/index.html)
10.  [Linux资源管理之cgroups简介](https://tech.meituan.com/2015/03/31/cgroups.html)