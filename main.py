from dataclasses import field
from typing import Callable
import flet as ft


@ft.control
class Task(ft.Column):
    task_name: str = ""
    on_status_change: Callable[[], None] = field(default=lambda: None)
    on_delete: Callable[["Task"], None] = field(default=lambda task: None)

    def init(self):
        self.completed = False

        self.display_task = ft.Checkbox(
            value=False,
            label=self.task_name,
            on_change=self.status_changed,
            expand=True,
        )

        self.edit_name = ft.TextField(expand=1)

        # Display view
        self.display_view = ft.Container(
            padding=12,
            border_radius=12,
            bgcolor=ft.Colors.WHITE10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.display_task,
                    ft.Row(
                        spacing=6,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.CREATE_OUTLINED,
                                icon_color=ft.Colors.BLUE_300,
                                tooltip="Edit",
                                on_click=self.edit_clicked,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=ft.Colors.RED_300,
                                tooltip="Delete",
                                on_click=self.delete_clicked,
                            ),
                        ],
                    ),
                ],
            ),
        )

        # Edit view
        self.edit_view = ft.Container(
            visible=False,
            padding=12,
            border_radius=12,
            bgcolor=ft.Colors.WHITE10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.edit_name,
                    ft.IconButton(
                        icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                        icon_color=ft.Colors.GREEN_300,
                        tooltip="Save",
                        on_click=self.save_clicked,
                    ),
                ],
            ),
        )

        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.on_status_change()

    def delete_clicked(self, e):
        self.on_delete(self)


@ft.control
class TodoApp(ft.Column):
    def init(self):
        self.new_task = ft.TextField(
            hint_text="What needs to be done?",
            expand=True,
            border_radius=12,
            filled=True,
            bgcolor=ft.Colors.WHITE10,
        )

        self.tasks = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO)

        # Filter tabs
        self.filter = ft.TabBar(
            tabs=[
                ft.Tab(label="All"),
                ft.Tab(label="Active"),
                ft.Tab(label="Completed"),
                
            ],

        )

        # ✅ FIXED: length added for old Flet versions
        self.filter_tabs = ft.Tabs(
            length=3,   # <<< FIX
            selected_index=0,
            on_change=lambda e: self.update(),
            content=self.filter,
        )

        self.width = 600
        self.spacing = 20

        self.controls = [
            ft.Text("📝 My To-Do List", size=26, weight=ft.FontWeight.BOLD,color=ft.Colors.WHITE),
            
            ft.Row(
                spacing=10,
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        bgcolor=ft.Colors.BLUE_400,
                        on_click=self.add_clicked,
                    ),
                ],
            ),
            ft.Container(
                padding=14,
                border_radius=16,
                bgcolor=ft.Colors.BLACK,
                content=ft.Column(
                    spacing=20,
                    controls=[
                        self.filter_tabs,
                        self.tasks,
                    ],
                ),
            ),
        ]

    def add_clicked(self, e):
        if self.new_task.value.strip() == "":
            return
        task = Task(
            task_name=self.new_task.value,
            on_status_change=self.task_status_change,
            on_delete=self.task_delete,
        )
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def task_status_change(self):
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def before_update(self):
        status = self.filter.tabs[self.filter_tabs.selected_index].label.lower()
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and not task.completed)
                or (status == "completed" and task.completed)
            )


def main(page: ft.Page):
    page.title = "To-Do App"
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    app = TodoApp()
    page.add(app)
   


ft.run(main)
