class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str, 
                 duration: float,  # длительность тренировки
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки в часах
                 weight: float) -> None:  # вес спортсмена

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return (self.distance)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.speed = self.get_distance() / self.duration
        # self.speed = round(self.speed, 3)
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(
            'Running', self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())

        return info_message


class Running(Training):
    """ Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    MIN_IN_H = 60

    def get_spent_calories(self) -> float:
        self.calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
        * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
        * self.weight / self.M_IN_KM * (self.duration * self.MIN_IN_H))
        return self.calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(
            'Running', self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())

        return info_message


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    CM_IN_M = 100
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,) -> None:

        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed_msec = (self.get_mean_speed() * self.KMH_IN_MSEC)
        return (self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                + (speed_msec ** 2 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * (self.duration * self.MIN_IN_H)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(
            'SportsWalking', self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())

        return info_message


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SPEED = 1.1
    CALORIES_MEAN_SPEED_MULT = 2
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,  # длина бассейна в метрах
                 count_pool: int) -> None:  # сколько раз переплыл бассейн

        super().__init__(action, duration, weight)

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        self.speed = (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)
        return self.speed

    def get_spent_calories(self):
        self.calories = ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED)
                * self.CALORIES_MEAN_SPEED_MULT
                * self.weight * self.duration)
        return self.calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(
            'Swimming', self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())

        return info_message


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    type_training: dict[str, type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking,
                                                }

    return type_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


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
        main(training)
