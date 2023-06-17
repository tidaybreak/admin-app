#!/bin/bash


cd ..

PROJECT_NAME="dcim-app"

if [[ -f $PROJECT_NAME.tar.gz ]]
  then
    echo "已经存在$PROJECT_NAME.tar.gz文件,这里对它进行删除操作!"
    rm $PROJECT_NAME.tar.gz
fi

echo "开始打包$PROJECT_NAME"

tar zcf $PROJECT_NAME.tar.gz $PROJECT_NAME
echo "结束打包$PROJECT_NAME"

