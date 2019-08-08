function tableSpan(rsData, lColumn, rowFrom=0, rowTo=-1) {
    /*
    用于表格行合并单元格
    rsData:     需要行合并的二维数组
    lColumn:    需要合并的列序号列表：
                序号从0开始
                前列合并了，后列才允许合并
                例如：[0,1,3]，表示合并第0、1、3列，且后面的合并依赖前一列的合并结果
    rowFrom:    起始行，默认0
    rowTo:      截止行，默认-1，代表最后一行
     */
    var i = 0;
    var j = 0;
    var k = 0;
    var preCol = true;

    // 参数校验
    if(rowFrom < 0)
        // 起始行最小为0
        rowFrom = 0;
    if(rowTo >= rsData.length || rowTo === -1)
        // 截止行最大为最后一行
        rowTo = rsData.length - 1;
    for(i=0; i<lColumn.length; i++){
        for(j=rowFrom; j<=rowTo; j++)
            if(lColumn[i] >= rsData[j].length){
                // 合并列序号超出范围，删除
                lColumn.splice(i, 1);
                i--;
                break
            }
    }

    // 初始化计算值，只生成行范围内的控制数据
    var rsSpan = [];
    for(i=rowFrom; i<=rowTo; i++){
        rsSpan.push([]);
        for (j = 0; j < rsData[i].length; j++)
            rsSpan[rsSpan.length - 1].push(1)
    }

    // 计算跨行数据
    for(i=0; i<lColumn.length; i++)
        for(j=rowFrom+1; j<=rowTo; j++){
            if(i === 0)
                // 第一列不依赖其他列
                preCol = true;
            else if(rsSpan[j-rowFrom][lColumn[i-1]] === 0)
                // 其他列必须前一列已合并，才允许合并
                preCol = true;
            else
                preCol = false;
            if (preCol && rsData[j][lColumn[i]] === rsData[j - 1][lColumn[i]]) {
                rsSpan[j - rowFrom][lColumn[i]] = 0;
                for (k = j - 1; k >= rowFrom; k--)
                    if (rsSpan[k - rowFrom][lColumn[i]] > 0) {
                        // 合并的行加到上一行，如果上一行也被合并，则继续往上找，依次类推
                        rsSpan[k - rowFrom][lColumn[i]]++;
                        break
                    }
            }
        }

    return rsSpan
}