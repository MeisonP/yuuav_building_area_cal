# README 
是基于参考物做标定的面积ref_area， 人工手动描边。

### 使用步骤 （依赖于第三方平台来做轮廓描绘，以及提供contours坐的api接口）
* 1）先安装 yuuav_building_area_draw
> cd 到 yuuav_building_area_draw 根目录，并依次执行：
>
meteor npm install
>
meteor npm start
* 2）用 yuuav_building_area_draw 提取/描绘 building的轮廓
>
a.将图放到其输入路径（可在setting.json中修改）例如：～/sse-images/**.png
>
b.打开meteor 启动后的 url，选择对应的图片进行轮廓提取，contours的json文件会以url 接口的形式提供使用
>
c.下载轮廓描完之后的图片.例如：~/Download/**_segmentation.png
* 2）yuuav_building_area_cal 添加下载下来的图片，通过前端交互计算面积。
