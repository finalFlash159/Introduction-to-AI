from collections import deque
import pydot
import argparse
import os

# Set it to bin folder of graphviz
os.environ["PATH"] += os.pathsep + '/opt/homebrew/bin'

options = [(1,0), (0, 1), (1, 1), (0, 2), (2, 0)] # trạng thái của số người và số quỷ khi di chuyển qua lại 2 bờ, mỗi lần chỉ chỗ 1 hoặc 2 chỗ

Parent = dict()
graph = pydot.Dot(graph_type = 'graph', strict = False, bgcolor='#fff3af',
                  label='fig: Missionaries and Cannibal State Space Tree')
# To track node (theo dõi)
i = 0
arg = argparse.ArgumentParser() # xử lý các tham số truyền vào khi chạy trương trình từ command line (terminal)
arg.add_argument('-d', '--depth', required = False, # xác định độ sâu tối đa của đồ thị trong không gian trạng thái
                 help = 'Maximum depth upto which ypu want to generate Space State Tree')

args = vars(arg.parse_args()) # phân tích và lấy các đối số từ dòng lệnh và đưa chúng vào một dictionary để dễ dàng truy xuất

max_depth = int(args.get('depth', 20))

def is_valid_move(number_missionaries, number_cannibals): # kiểm tra số lượng nhà truyền giáo và ăn thịt người có hợp lệ không 
    """
    Check if number constraints are satisfied
    """
    return (0 <= number_missionaries <= 3) and (0 <= number_cannibals <= 3)

def write_image(file_name = 'state_space'): # lưu đồ thị vào file
    try:
        graph.write_png(f"{file_name}_{max_depth}.png")
    except Exception as e:
        print('Error while writing file', e)
        print(f"File {file_name}_{max_depth}.png successfully written.")

def draw_edge(number_missionaries, number_cannibals, side, depth_level, node_num): # vẽ các cạnh nối giữa các nút
    # Các tham số của hàm đại diện cho trạng thái của một nút trong đồ thị:
    # - `number_missionaries`: Số lượng nhà truyền giáo ở một bên bờ sông
    # - `number_cannibals`: Số lượng kẻ ăn thịt người ở một bên bờ sông
    # - `side`: Bờ sông mà thuyền đang ở (ví dụ: 0 là bờ trái, 1 là bờ phải)
    # - `depth_level`: Độ sâu của nút trong cây không gian trạng thái
    # - `node_num`: Số thứ tự của nút (để phân biệt các trạng thái khác nhau tại cùng một độ sâu)
    u, v = None, None
    if Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)] is not None: # kiểm tra nút cha của nút hiện tại có tồn tại không
        # Nếu nút cha tồn tại, tức là nút hiện tại không phải là nút gốc.
        # Tạo nút `u` là nút cha của nút hiện tại.
        u = pydot.Node(str(Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)]),
                       label = str(Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)][:3]))
        graph.add_node(u) # thêm nút 'u' vào đồ thị

        # tạo nút `v` là nút hiện tại
        v = pydot.Node(str((number_missionaries, number_cannibals, side, depth_level, node_num)),
                       label= str((number_missionaries, number_cannibals, side ))) # depth_level, node_num
        graph.add_node(v)

        # tạo cạnh nối từ nút `u` đến nút `v`
        edge = pydot.Edge(str(Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)]),
                           str((number_missionaries, number_cannibals, side, depth_level, node_num)), dir = 'forward')
        graph.add_edge(edge) 
    else:
        # For start node
        # nếu nút hiện tại là nút gốc
        # tạo nút `v`
        v = pydot.Node(str((number_missionaries, number_cannibals, side, depth_level, node_num)),
                       label = str((number_missionaries, number_cannibals, side)))
        graph.add_node(v)
    return u, v

def is_start_state(number_missionaries, number_cannibals, side): # trạng thái ban đầu ở bờ bên trái (3 nhà truyền giáo, 3 ăn thịt người, thuyền ở bờ bên trái)
    return (number_missionaries, number_cannibals, side) == (3, 3, 1)

def is_goal_state(number_missionaries, number_cannibals, side): # trạng thái đích ở bờ bên trái (0 nhà truyền giáo, 0 ăn thịt người, thuyền ở bờ bên phải)
    return (number_missionaries, number_cannibals, side) == (0, 0, 0)

def number_of_cannibals_exceeds(number_missionaries, number_cannibals): 
    # kiểm tra xem số ăn thịt người có nhiều hơn số nhà truyền giáo hay không
    # ở cả hai bên bờ
    number_missionaries_right = 3 - number_missionaries                   
    number_cannibals_right = 3 - number_cannibals
    return number_missionaries > 0 and number_cannibals > number_missionaries\
    or (number_missionaries_right > 0 and number_cannibals_right > number_missionaries_right)


def generate(): # tạo đồ thị theo độ sâu đã nhập trong không gian trạng thái
    global i
    q = deque()
    node_num = 0
    q.append((3, 3, 1, 0, node_num)) # thêm trạng thái bắt đầu vào hàng đợi

    Parent[(3, 3, 1, 0, node_num)] = None

    while q: # nếu hàng đợi không rỗng
        number_missionaries, number_cannibals, side, depth_level, node_num = q.popleft() # lấy ra nút ở đầu hàng đợi
        # print(number_missionaries, number_cannibals)
        # # Draw Edge from u -> v
        # Where u = Parent(v)
        # and v = (number_missionaries, number_cannibals, side, depth_level)

        u, v = draw_edge(number_missionaries, number_cannibals, side, depth_level, node_num) # tạo các nút và cạnh
        # u = v

        if is_start_state(number_missionaries, number_cannibals, side):
            v.set_style("filled")
            v.set_fillcolor("blue") #fontcolor
        elif is_goal_state(number_missionaries, number_cannibals, side):
            v.set_style("filled")
            v.set_fillcolor("green")
            continue
            # return True
        elif number_of_cannibals_exceeds(number_missionaries, number_cannibals): # nếu không thoả điều kiện (ăn thịt người > nhà truyền giáo)
            v.set_style("filled") 
            v.set_fillcolor("red")
            continue
        else:
            v.set_style("filled") # thoả điều kiện
            v.set_fillcolor("orange")

        if depth_level == max_depth: # Khi đạt đến độ sâu tối đa (max_depth), hàm sẽ dừng mở rộng và trả về True
            return True

        op = -1 if side == 1 else 1 # op là một giá trị cho biết thuyền đang ở bờ nào (1 là bờ đích, -1 là bờ bắt đầu).
        can_be_expanded = False

        i = node_num
        for x, y in options: 
            next_m, next_c, next_s = number_missionaries + op * x, number_cannibals + op * y, int(not side) # cập nhật trạng thái cho bờ bên trái sau khi di chuyển
            # in(not side) đổi vị trí nếu side == 1 thì trả về False <=> int(False) == 0 và ngược lại
            
            # Điều kiện đảm bảo rằng trạng thái mới không phải là nút cha của trạng thái hiện tại (tránh quay lại trạng thái cũ).
            if Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)] is None or \
               (next_m, next_c, next_s) != Parent[(number_missionaries, number_cannibals, side, depth_level, node_num)][:3]:

                # nếu trạng thái di chuyển hợp lệ, trạng thái mới sẽ được thêm vào hàng đợi q, đồng thời lưu lại quan hệ cha-con trong Parent.
                if is_valid_move(next_m, next_c):
                    can_be_expanded = True
                    i += 1
                    q.append((next_m, next_c, next_s, depth_level + 1, i))
                    # keep track of parent
                    Parent[(next_m, next_c, next_s, depth_level + 1, i)] = \
                        (number_missionaries, number_cannibals, side, depth_level, node_num)

        if not can_be_expanded: # Nếu không có di chuyển hợp lệ nào, nút sẽ được đặt thành màu xám, cho biết nút này không thể mở rộng thêm.
            v.set_style("filled")
            v.set_fillcolor("gray")

    return False

if __name__ == "__main__": # Nếu gọi hàm generate() thành công, hàm write_image() sẽ được gọi để lưu đồ thị đã vẽ dưới dạng hình ảnh.
    if generate():
        write_image()

