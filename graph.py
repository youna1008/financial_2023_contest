class Graph():
    graph = dict()

    def __init__(self, data, class_dict, min_count=2, max_group=2):
        self.result = dict()
        self.data = data
        self.class_dict = class_dict
        self.min_count = min_count
        self.max_group = max_group
        self.big_group_result = set()
        self.f_index = dict()


    def filter_graph(self, feature, index=None):
        # 각 feature에 대한 인덱스 집합
        self.f_index = dict()
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
                self.f_index[f'{column}_{value}'] = set(data[data[column] == value]['index'])

        return self.f_index
    
    def merge_f_graph(self, feature):
        temp = dict()
        c_list = list()

        group_list = self.f_index.keys()

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
            group_result = '-'.join(c_list)
            self.big_group_result.add((cls_set, group_result, self.f_index[group]))

