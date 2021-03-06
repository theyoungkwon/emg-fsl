import os
import numpy as np


class DataLoader:
    def __init__(self) -> None:
        self.participants_count = 12
        self.scenarios_count = 3
        self.gestures_count = 5
        super().__init__()
        self.raw_data = {}
        for i in range(self.gestures_count):
            self.raw_data[str(i + 1)] = []

    # None for all participants/scenarios (default behavior)
    def load_files(self, participants=None, scenarios=None, gestures=None):

        if participants is None:
            participants = list(range(1, self.participants_count + 1))
        if scenarios is None:
            scenarios = list(range(1, self.scenarios_count + 1))
        if gestures is None:
            gestures = list(range(1, self.gestures_count + 1))

        for participant in participants:
            for scenario in scenarios:
                _dir = f"../Data/p{participant}_s{scenario}/"
                print(_dir)
                for file in os.listdir(_dir):
                    label = int(file[1])
                    if label in gestures:
                        print(file)
                        record = np.loadtxt(_dir + file)
                        self.raw_data[str(label)].append(record[:, :8])

    def get_xy(self, window_length=100, overlap=0.5):
        x = []
        y = []

        for label in self.raw_data:
            if self.raw_data[label] is None:
                continue
            for record in self.raw_data[label]:
                start = 0
                while start + window_length <= len(record):
                    datapoint = record[start:start + window_length]
                    x.append(datapoint)
                    y.append(int(label))
                    start += window_length - int(overlap * window_length)

        return x, y

    def get_xy_train_test(self, window_length=100, overlap=0.5, train_ratio=0.9):
        train_X = []
        train_y = []
        test_X = []
        test_y = []
        for label in self.raw_data:
            if self.raw_data[label] is None:
                continue

            for record in self.raw_data[label]:
                start = 0
                X = []
                y = []
                while start + window_length <= len(record):
                    datapoint = record[start:start + window_length]
                    X.append(datapoint)
                    y.append(int(label))
                    start += window_length - int(overlap * window_length)

                cut = int(len(X) * train_ratio)
                train_X.extend(X[:cut])
                train_y.extend(y[:cut])
                intertwined_gap = int(np.ceil((1 / (1 - overlap)))) - 1
                test_X.extend(X[cut + intertwined_gap:])
                test_y.extend(y[cut + intertwined_gap:])


        return train_X, train_y, test_X, test_y

if __name__ == '__main__':
    dl = DataLoader()
    dl.load_files(participants=[1], scenarios=[1, 2], gestures=[1, 2, 3])
    dl.get_xy(window_length=50, overlap=0.5)
