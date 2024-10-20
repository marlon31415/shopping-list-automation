#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import random
from typing import Optional, List

from utils import (
    export_to_markdown,
    export_to_enex,
)


class Dish:
    def __init__(self, name: str, category: str, level: str, ingredients: List[str]):
        self.name = name
        self.category = category
        self.level = level
        self.ingredients = ingredients

    @classmethod
    def from_data(cls, name, data_dict):
        return cls(
            name=name,
            category=data_dict["category"],
            level=data_dict["level"],
            ingredients=data_dict["ingredients"],
        )


class ShoppingList:
    def __init__(self, dishes_file):
        self.dishes = []
        with open(dishes_file, "r") as file:
            loaded_dishes = yaml.safe_load(file)
            for dish_name, dish_data in loaded_dishes["dishes"].items():
                dish = Dish.from_data(dish_name, dish_data)
                self.dishes.append(dish)

    def choose_dishes(
        self,
        num_dishes: int,
        num_easy: Optional[int] = None,
        num_intermediate: Optional[int] = None,
        num_advanced: Optional[int] = None,
        desired_dishes: Optional[List[str]] = None,
    ):
        chosen_dishes = []
        if desired_dishes:
            chosen_dishes.extend(
                [dish for dish in self.dishes if dish.name in desired_dishes]
            )
        if num_easy:
            chosen_dishes.extend(
                random.sample(
                    [dish for dish in self.dishes if dish.level == "easy"], num_easy
                )
            )
        if num_intermediate:
            chosen_dishes.extend(
                random.sample(
                    [dish for dish in self.dishes if dish.level == "intermediate"],
                    num_intermediate,
                )
            )
        if num_advanced:
            chosen_dishes.extend(
                random.sample(
                    [dish for dish in self.dishes if dish.level == "advanced"],
                    num_advanced,
                )
            )
        if num_dishes - len(chosen_dishes) > 0:
            chosen_dishes.extend(
                random.sample(
                    [
                        dish
                        for dish in self.dishes
                        if dish not in chosen_dishes and dish.level != "advanced"
                    ],
                    num_dishes - len(chosen_dishes),
                )
            )
        return chosen_dishes

    def generate_shopping_list(self, chosen_dishes: List[Dish]):
        shopping_list = {"dishes": []}
        for dish in chosen_dishes:
            shopping_list["dishes"].append(dish.name)
            for ingredient in dish.ingredients:
                ingredient_name = ingredient["name"]
                ingredient_class = ingredient["class"]
                if ingredient_class in shopping_list:
                    if ingredient_name in shopping_list[ingredient_class]:
                        shopping_list[ingredient_class][ingredient_name] += 1
                    else:
                        shopping_list[ingredient_class][ingredient_name] = 1
                else:
                    shopping_list[ingredient_class] = {}
                    shopping_list[ingredient_class][ingredient_name] = 1
        return shopping_list

    def generate_list(
        self,
        num_dishes: int,
        num_easy: Optional[int] = None,
        num_intermediate: Optional[int] = None,
        num_advanced: Optional[int] = None,
        desired_dishes: Optional[List[str]] = ["sushi"],
    ):
        # ! exception handling
        if num_dishes > len(self.dishes):
            raise ValueError("Number of dishes requested exceeds available dishes.")
        if num_easy or num_intermediate or num_advanced or desired_dishes:
            num_desired_dishes = len(desired_dishes) if desired_dishes != None else 0
            non_none_values = [
                i
                for i in (
                    num_easy,
                    num_intermediate,
                    num_advanced,
                )
                if i is not None
            ]
            num_specified_dishes = sum(non_none_values) + num_desired_dishes
            if num_specified_dishes > num_dishes:
                raise ValueError(
                    "Number of specified dishes exceeds number of dishes requested."
                )

        # ! choose dishes
        chosen_dishes = self.choose_dishes(
            num_dishes, num_easy, num_intermediate, num_advanced, desired_dishes
        )
        # ! create shopping list with sections
        shopping_list = self.generate_shopping_list(chosen_dishes)
        return shopping_list


if __name__ == "__main__":
    shopping_list = ShoppingList("./res/dishes_example.yaml")
    sl = shopping_list.generate_list(
        num_dishes=4, num_easy=1, num_intermediate=1, num_advanced=0
    )

    print(sl)

    export_to_markdown(sl)
    export_to_enex(sl)
