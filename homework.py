# from dataclasses import
# import types


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,  # длительность тренировки
                 distance,
                 speed,
                 calories,
                 ) -> None:
        pass

    def get_message():
        # return (f'Тип тренировки: {self.training_type}; Длительность: '
        # '{self.duration} ч.; Дистанция: {self.distance} км; Ср. скорость:'
        # '{self.speed} км/ч; Потрачено ккал: {self.calories}.')
        pass


class Training:
    """Базовый класс тренировки."""
    # LEN_STEP:float = 0.65
    # M_IN_KM:int = 1000
    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки в часах
                 weight: float) -> None:  # вес спортсмена

        # self.action = action
        # self.duration = duration
        # self.weight = weight
        # self.distance = distance
        # self.speed = speed
        # self.calories = calories
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        # return self.action * (self.LEN_STEP / self.M_IN_KM)
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # return self.distance / self.duration
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        
        pass


class Running(Training):
    """ Тренировка: бег."""
    # CALORIES_MEAN_SPEED_MULTIPLIER = 18
    # CALORIES_MEAN_SPEED_SHIFT = 1.79

    # return ((CALORIES_MEAN_SPEED_MULTIPLIER * self.speed +
    # CALORIES_MEAN_SPEED_SHIFT)* self.weight / self.M_IN_KM * self.duration)
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,) -> None:

        super().__init__(action, duration, weight)

        self.height = height

        # XXXX = 0.035
        # YYYY = 0.029

        # return (0.035 * self.weight + (self.speed**2 / self.height)* 0.029
        # * self.weight) * self.duration


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,  # длина бассейна в метрах
                 count_pool: int) -> None:  # сколько раз переплыл бассейн

        super().__init__(action, duration, weight)

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self):

        # return (self.speed + 1.1) * 2 * self.weight * self.duration
        pass

    def get_mean_speed(self):
        # self.LEN_STEP:float = 1.38
        # return self.length_pool * self.count_pool / self.M_IN_KM
        # / self.duration
        pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    # print(workout_type, data)

    type_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    training = type_training.get(workout_type)

    if training == Swimming:
        obj = Swimming(data[0], data[1], data[2], data[3], data[4])
    elif training == Running:
        obj = Running(data[0], data[1], data[2])
    elif training == SportsWalking:
        obj = SportsWalking(data[0], data[1], data[2], data[3])
    else:
        print('ERROR')

    return obj


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()


if __name__ == '__main__':
    packages = [
        # action, duration, weight, length_pool, count_pool
        ('SWM', [720, 1, 80, 25, 40]),

        # action, duration, weight
        ('RUN', [15000, 1, 75]),

        # action, duration, weight
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        print(training)
        main(training)
