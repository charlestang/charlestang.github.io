---
title: Yii框架中验证器的allowEmpty属性
tags:
  - usage
  - yii
id: '435'
categories:
  - - something-about-daily-work
    - Yii
  - - 工作相关
date: 2011-05-18 16:13:08
---

Yii框架自带验证器这个包，提供了一组常见各类属性的验证器。如果使用Gii代码生成工具创建model，会根据数据库字段的属性默认生成一些验证器的配置。在配置验证器的时候，很多验证器都有以后属性叫做allowEmpty，这个属性的真正逻辑却不是看上去的那个意思。
<!-- more -->
数据库里的字段，有个属性，叫NULL，就是字段是否允许为空值，allowEmpty听起来跟这个NULL的约束是一样的，但是实际看验证器的代码：

```php

protected function validateAttribute($object,$attribute)
{
$value=$object->$attribute;
if($this->allowEmpty && $this->isEmpty($value))
return;

if(function_exists('mb_strlen') && $this->encoding!==false)
$length=mb_strlen($value,$this->encoding ? $this->encoding : Yii::app()->charset);
else
$length=strlen($value);
if($this->min!==null && $length<$this->min)
{
$message=$this->tooShort!==null?$this->tooShort:Yii::t('yii','{attribute} is too short (minimum is {min} characters).');
$this->addError($object,$attribute,$message,array('{min}'=>$this->min));
}
if($this->max!==null && $length>$this->max)
{
$message=$this->tooLong!==null?$this->tooLong:Yii::t('yii','{attribute} is too long (maximum is {max} characters).');
$this->addError($object,$attribute,$message,array('{max}'=>$this->max));
}
if($this->is!==null && $length!==$this->is)
{
$message=$this->message!==null?$this->message:Yii::t('yii','{attribute} is of the wrong length (should be {length} characters).');
$this->addError($object,$attribute,$message,array('{length}'=>$this->is));
}
}

```

来看其中一个细节：

```php

if($this->allowEmpty && $this->isEmpty($value)) return;

```

这一行什么意思，如果被验证属性为空，就认为完全合法，立刻返回，但是如果allowEmpty为false的话，就要通过函数后续的所有验证条件。那么对于一个传入的空值来说，allowEmpty无论是true还是false，极有可能都不会报错，上面节选的验证器是StringValidator，如果我没有设定min的值，那么一个空串在allowEmpty为false的情况下，还是不会报任何错误的。

如果希望一个属性值不能为空，最好还是用RequiredValidator来验证，allowEmpty是不靠谱的，建议一般就采取allowEmpty的默认值true，可以节省几次判断。然后不要中了Yii的这个小陷阱噢~~希望Yii的后续版本可以让这个功能显得更加自然一点，不要让我猜谜语。