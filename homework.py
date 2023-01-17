from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str  # тип
    duration: float  # длительность
    distance: float  # дистанция
    speed: float  # средняя скорость
    calories: float  # потрачено ккал

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


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
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(
            type(self).__name__,
            self.duration,
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
                         * self.get_mean_speed()
                         + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                         / self.M_IN_KM * (self.duration * self.MIN_IN_H))
        return self.calories


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
        return (self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                   / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * (self.duration * self.MIN_IN_H)


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


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    type_training: dict[str, type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}

    if workout_type not in type_training:  # guard 1
        raise ValueError("Мы так не тренируемся! Можно только так:",
                         *type_training.keys())

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
