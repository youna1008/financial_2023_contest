class Graph():
    graph = dict()

    def __init__(self, data, class_dict, min_count=2, max_group=2):
        self.result = dict()
        self.data = data
        self.class_dict = class_dict
        self.min_count = min_count
        self.max_group = max_group
        self.big_group_result = set()
        self.mid_group_result = set()
        self.small_group_result = set()
        self.f_filter = dict()

    def filter_graph(self, feature, index=None):
        # 각 feature에 대한 인덱스 집합
        self.f_filter = dict()
        if index:
            data = self.data[self.data['index'] == index]
        
        else:
            data = self.data

        
        for column in feature:
            value_counts = data[column].value_counts()

            # 연결된 노드의 엣지가 min보다 작은 경우 제외
            value_counts = {key: value for key, value in value_counts.items() if value > self.min_count}

            # 연결된 노드의 cardinality가 낮은 경우 제외
            if len(value_counts) > self.max_group:
                continue

            for value, count in value_counts.items():
                self.f_filter[f'{column}_{value}'] = set(data[data[column] == value]['index'])

        return self.f_filter
    
    # 특정 index에 대해서 다시한번 진행 (얘는 min을 적용 안하나?)
    def merge_f_graph(self, feature, t, group_key):
        c_list = list()

        group_list = self.f_filter.keys()
        total_group_result = set()

        # cls_set은 사용하는 클래스들을 분류
        for group in group_list:
            cls_set = set()
            data = self.data[self.data['index'].isin(self.index[group])]

            for column in feature:
                value_counts = data[column].value_counts()

                if len(value_counts) > self.max_group:
                    continue

                for value, count in value_counts.items():
                    c_list.append(f"{column}_{value}")

                for cls in feature:
                    if cls in column:
                        cls_set.add(cls)
                
            # 각각 어캐 담아야할지 고민해봐야 함.
            # 앞에는 중분류로 가기위함, 뒤에는 그룹의 총 묶인거, 마지막은 인덱스
            # 중복제거 한번 해줘야하나 싶기도 함
            group_result = group_key + '-' + '-'.join(c_list)
            total_group_result.add((cls_set, group_result, self.f_index[group]))

        if t == "big":
            self.big_group_result = total_group_result
        if t == "mid":
            self.mid_group_result = total_group_result
        if t == "small":
            self.small_group_result = total_group_result

    # f_filter는 temp데이터여서 없애는 방식 도입할 수 있을듯
    # mid랑 small이랑 big이 대입하는게 거의 비슷해서 같은 함수로 사용할 수 있을지도?
    # 내일 얘기해보면서 코드 작성하기?
    def mid_group_filter(self):
        for cls, group_key, idx in self.big_group_result:
            # mid그룹의 column가져오기
            columns = self.get_key(cls, "mid")

            filter_data = self.filter_graph(columns, idx)
            self.merge_f_graph(columns, "mid", group_key)
            
        # self.big_group_result = {} # 메모리 부족할 때 
    def small_group_filter(self):
        for cls, group_key, idx in self.mid_group_result:
            # mid그룹의 column가져오기
            columns = self.get_key(cls, "small")

            filter_data = self.filter_graph(columns, idx)
            self.merge_f_graph(columns, "small", group_key)

        # self.mid_group_result = {} # 메모리 부족할 때

    def get_key(self, cls, t):
        result = set()
        big = self.class_dict.keys()
        for b in big:
            if t == "big":
                if b in cls:
                    result.add(b)
 
            mid = self.class_dict[b].keys()
            for m in mid:
                if t == "mid":
                    if m in cls:
                        result.add(m)

                if t == "small":
                    for s in self.class_dict[b][m]:
                        if s in cls:
                            result.add(s)
        
        return result