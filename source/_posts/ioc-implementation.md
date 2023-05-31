---
title: 怎么实现 Inversion of Control (IoC)？
tags:
  - design pattern
  - object oriented
id: '1006'
categories:
  - - 工作相关
date: 2021-02-28 11:24:34
---

前面花了很多篇幅去讲了 IoC 这个概念的问题，最后，还是要落实到实现上。通过分析和推理，我们了解到 IoC 的本质还是为了解耦和复用，而这个核心，最后落实到而组件和对象的创建和组装上面。

《[什么是 Inversion of Control？](https://sexywp.com/inversion-of-control-ioc.htm)》

《[为什么需要 Inversion of Control？](https://sexywp.com/why-need-inversion-of-control-ioc.htm)》

了解了这些，就不会“乱花渐欲迷人眼”，无论是 Spring 强调的 IoC Container 也好，还是 Martin 老爷说的 Service Locator，Dependency Injection，其背后，目的是统一的。无非是手段是多样的。那么，我们只要逐一去了解这些手段即可。
<!-- more -->
## Dependency Injection (DI)

说到 DI，这就是一个真正的设计模式了，其核心思想是，在一个对象内部，使用依赖的时候，不是去创建它，而是从对象的外部注入进来这个依赖。对被依赖对象的使用，完全由协议决定，一般来说是接口。

把一个依赖对象注入进去的方法大概有三种：

*   从构造函数注入
*   使用属性注入
*   使用接口注入

### 从构造函数注入

比较常见的一个注入的方式就是从构造函数注入，把被依赖的对象声明成属性，在自己被构造的时候，从外部赋值，直接完成注入，这里我就用 PHP 的 Yii 框架来举例子了，但是这跟语言是无关的。

```php
class Action extends Component
{
    /**
     * @var string ID of the action
     */
    public $id;
    /**
     * @var Controller\yii\web\Controller\yii\console\Controller the controller that owns this action
     */
    public $controller;


    /**
     * Constructor.
     *
     * @param string $id the ID of this action
     * @param Controller $controller the controller that owns this action
     * @param array $config name-value pairs that will be used to initialize the object properties
     */
    public function __construct($id, $controller, $config = [])
    {
        $this->id = $id;
        $this->controller = $controller;
        parent::__construct($config);
    }

    //....
}
```

这是 MVC 里面的 Action 的构造函数，我们可以看到，Action 需要依赖调用自身的 Controller，所以用 controller 的抽象类声明了一个属性，在此 Action 被被构造的时候，通过构造器对 controller 这个属性进行赋值。

### 从属性注入

从属性注入，可能是比从构造器更为普遍的一种做法，我是这么理解这个问题的，因为，一个对象可能依赖很多，这就带来两个问题，如果把所有的依赖都堆在构造器的话，那构造函数就会很长很长，那就十分难看了。

第二点，一个对象具有的功能可能有几个，每个功能依赖的组合不一样，A 功能依赖甲乙丙，而 B 功能依赖丁戊己，这么一来，在构造的时候，我到底传入哪几个被依赖对象呢？都传的话，可能就造成了浪费，也可能我在构造的一刻还不知道到底即将使用哪个功能。

于是，按需从属性进行注入，就变成一种很自然的选择了。

```php
class BaseObject implements Configurable
{
    //……

    /**
     * Returns the value of an object property.
     *
     * Do not call this method directly as it is a PHP magic method that
     * will be implicitly called when executing `$value = $object->property;`.
     * @param string $name the property name
     * @return mixed the property value
     * @throws UnknownPropertyException if the property is not defined
     * @throws InvalidCallException if the property is write-only
     * @see __set()
     */
    public function __get($name)
    {
        $getter = 'get' . $name;
        if (method_exists($this, $getter)) {
            return $this->$getter();
        } elseif (method_exists($this, 'set' . $name)) {
            throw new InvalidCallException('Getting write-only property: ' . get_class($this) . '::' . $name);
        }

        throw new UnknownPropertyException('Getting unknown property: ' . get_class($this) . '::' . $name);
    }

    /**
     * Sets value of an object property.
     *
     * Do not call this method directly as it is a PHP magic method that
     * will be implicitly called when executing `$object->property = $value;`.
     * @param string $name the property name or the event name
     * @param mixed $value the property value
     * @throws UnknownPropertyException if the property is not defined
     * @throws InvalidCallException if the property is read-only
     * @see __get()
     */
    public function __set($name, $value)
    {
        $setter = 'set' . $name;
        if (method_exists($this, $setter)) {
            $this->$setter($value);
        } elseif (method_exists($this, 'get' . $name)) {
            throw new InvalidCallException('Setting read-only property: ' . get_class($this) . '::' . $name);
        } else {
            throw new UnknownPropertyException('Setting unknown property: ' . get_class($this) . '::' . $name);
        }
    }

    //……
}
```

上面展示了 Yii 框架里面 BaseObject 的一段实现，这里是 PHP 的魔术方法，实现了属性这个抽象概念，当我们使用 `->` 操作符引用一个符号的时候，对象就会调用魔术方法，先按照属性的方式去理解这个符合。这个类是 Yii 框架里所有类的基类，所有的类都支持使用属性进行注入。

### 使用接口注入

接口注入的方法，其实就是把注入用的方法，单独由接口定义出来，然后需要注入的对象类，实现此接口即可。我在 Yii 框架里没有找到具体的例子，主要是因为 Yii 框架因为是 PHP 语言，有别的注入方法，所以，无法举例了，当然这个例子本身也比较难以理解。

这里我直接[引用 Martin 老爷的 Java 的例子](https://martinfowler.com/articles/injection.html#InterfaceInjection)吧。

从这个例子里，我们可以看出，使用接口注入的方式，可以让容器不关注对象本身的类型，抽象地来完成注入，可能在某些场合会带来一些方便。

## DI 容器

我们一直在谈依赖注入的问题，前天主要探讨了其客体，就是作为被注入对象，是怎么实现的。也不得不谈及主体，就是谁来完成注入工作的事情。一般来说，大家更喜欢讨论前面一个问题，因为我们都是框架的用户，只要了解前面那一半问题，就可以愉快地代码和工作了。后面这一半一般是框架的责任。

不过为了文章的完整性，不得不做一些简短地讨论。所谓的 DI 容器，我猜测很多号称自己是 IoC Container 的框架，也一定程度在说这个。因为 DI 就是 IoC 思想的一种实现思路。我们不难想到，这个容器首先要是一个注册表，允许把各种对象注入进来，除了这个对象的名字 ID，就是这个对象的依赖，容器的责任就是在取得这个对的时候，把依赖都创建好，然后注入进去，再返回对象。所以，很显然，这个容器要具有“解决依赖”的功能（Resolve Dependency）。

遇到一个新的框架，我们可以看看其 DI 容器的实现，就可以了解到这个框架基本上如何处理对象的依赖，以及怎么实现依赖注入的功能。一般容器都会提供几个简单的接口，比如 register，get，有的还有 invoke 等等。

## Service Locator

这是另一种实现 IoC 的模式，也是来自 Martin 老爷。我怎么理解这个模式呢，和 DI 比较着理解的话，我觉得就是“主动”与“被动”的区别。在 DI 里面，我们无论是实现构造器，实现属性，还是实现接口，都是等着“别人”来给我的对象里注入我的依赖。

但是如果是对象自己主动去一个注册表里查询获取一个需要的依赖呢？这种模式就成了 Service Locator。这种模式本质上就是一个注册表，大家仍然可以把依赖注册进去，每个对象都有自己的 key，需要依赖的对象，在使用的时候，只要调用 locator 进行获取即可。

从这个功能描述上，我们可以理解出几个事实。第一，使用这种方式的时候，对象必须要依赖 Service Locator 对象，就引入了一个新的耦合，好在这是一个全局的唯一的对象，也只依赖这一个即可。

第二，Service Locator 也具有解决依赖的问题，在获取一个具名对象的时候，其依赖也要事先被解决好，然后构建出来。所以，在某些程度上和 DI 很像。这就使得两者并没有什么本质冲突，完全可以兼容，比如在 Yii 框架里面，就是使用 DI 来实现了 Service Locator 的 get 方法。

第三，比起被动模式来说，主动获取的模式，肯定要比被动模式更容易理解，也更家“按需加载”，更少意料之外的情况。但是，这显然会降低你实现的对象的复用性。因为在不同的框架里，Service Locator 都有各自的实现，显然也不方便引入多种 Service Locator 的实现，如果你实现的对象需要广泛分发使用的话，就很不适合使用这个模式。

## 后记

写到这里，基本已经写完了。不敢说讲得很正确或者讲得很深入，但是，我是下了一番心思的，看了很多的资料，国内的，国外的，然后汇聚成文，应该算讲得很**认真**。IoC 因为太过普遍，可能大家都略知一二，不过，就算完全不知道，也不影响大家使用框架，Spring 也好，Yii 框架也好，都不例外。但是，理解了这个概念，我认为再看框架代码的时候，就有一种了然的感觉。这种感觉让人欣喜，好像脑袋上一个灯泡“噔”的一声亮了那种。其他的各类模式和那种“可理解/可不理解”的概念，也有类似的特点。