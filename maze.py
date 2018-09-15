class Data_validate():
    '''
      判断输入是否规范的类
    '''
    def __init__(self,size,connect):
          self.size=size
          self.connect=connect
    def size_validate(self):
        size=self.size
        all=size.split()
        if len(all)==2:
            try:
                x=int(all[0])
                y=int(all[1])
                if x>0 and y>0:
                    return x,y
                else:
                    print('Number out of range​.​')

            except:
                print('Invalid number format​.​')
        else:
            print('Incorrect command format​.')
    def connect_validate(self):
        x_size,y_size=self.size_validate()
        connect=self.connect
        final_groups=[]
        groups=connect.split(';')
        if groups:
            for one_connect in groups:
                group=one_connect.split()
                if len(group)==2:
                      try:
                          group_detail1 = group[0].split(',')
                          group_detail2 = group[1].split(',')
                          x1=int(group_detail1[0])
                          y1=int(group_detail1[1])
                          x2=int(group_detail2[0])
                          y2 = int(group_detail2[1])
                          if x1>=0 and x1<x_size and y1>=0 and y1<y_size and x2>=0 and x2<x_size and y2>=0 and y2<y_size:
                              if (x1==x2 and abs(y1-y2)==1) or (abs(x1-x2)==1 and y1==y2):
                                  group_list=[(x1,y1),(x2,y2)]
                                  final_groups.append(group_list)
                                  if len(final_groups) == len(groups):
                                      return final_groups
                              else:
                                  print('Maze format error.')

                          else:
                              print('Number out of range​.')
                              break
                      except:
                          print('Invalid number format​.')
                          break

                else:
                 print('Incorrect command format​.​')
                 break
        else:
            print('Incorrect command format​.​')


class Get_size():
    '''
     获取道路网格的尺寸
    '''
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def create(self):
        x,y=self.x*2+1,self.y*2+1
        datas=[[] for i in range(x)]
        for a in range(0,x):
            for b in range(0,y):
                datas[a].append('[W]')
        return datas
    def begin_grid(self):
        datas=self.create()
        for row in datas[1:-1:2]:
            for i in range(0,len(row)):
                if (i+1)%2==0:
                    row[i]='[R]'
        return datas


class Get_connect():
    '''
    联通道路
    '''
    def __init__(self,datas,connet_list):
        self.datas=datas
        self.connect_list=connet_list
    def change(self):
        datas=self.datas
        for group_list in self.connect_list:
             begin_x1,begin_y1=group_list[0]
             begin_x2,begin_y2=group_list[1]
             actual_x1,actual_y1=begin_x1*2+1,begin_y1*2+1
             actual_x2,actual_y2=begin_x2*2+1,begin_y2*2+1
             if actual_x1==actual_x2 and actual_y1-actual_y2==2:
                 datas[actual_x1][actual_y2+1]='[R]'
             elif actual_x1==actual_x2 and actual_y2-actual_y1==2:
                 datas[actual_x1][actual_y1 + 1] = '[R]'
             elif actual_y1==actual_y2 and actual_x1-actual_x2==2:
                 datas[actual_x2+1][actual_y1] = '[R]'
             elif actual_y1 == actual_y2 and actual_x2 - actual_x1 == 2:
                 datas[actual_x1 + 1][actual_y1] = '[R]'
        return datas


if __name__=='__main__':
    while True:
        try:
            size = input('请输入迷宫道路网格​的尺寸（格式：x y）：')
            connest = input('请输入迷宫道路网格​的连通性定义（以英文分号“;”隔开）：')
            size_and_connect=Data_validate(size,connest)
            x,y=size_and_connect.size_validate()
            connect_list=size_and_connect.connect_validate()
            datas=Get_size(x,y).begin_grid()
            final=Get_connect(datas,connect_list).change()
            for row in final:
                row_standard=' '.join(row)
                print(row_standard)
            break
        except:
            print('错误信息如上，请从新输入')