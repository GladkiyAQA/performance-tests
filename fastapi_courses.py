from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel, RootModel

app = FastAPI()

courses_router = APIRouter(
    prefix="/api/v1/courses",
    tags=["courses-service"]
)


class CourseIn(BaseModel):
    """
    Входная модель для курса (без id).
    """
    title: str
    max_score: int
    min_score: int
    description: str


class CourseOut(CourseIn):
    """
    Выходная модель для курса (с id).
    """
    id: int


class CoursesStore(RootModel):
    """
    In-memory хранилище курсов.
    """
    root: list[CourseOut]

    def find(self, course_id: int) -> CourseOut | None:
        """Найти курс по ID."""
        return next((course for course in self.root if course.id == course_id), None)

    def create(self, course_in: CourseIn) -> CourseOut:
        """Создать новый курс и выдать id автоматически."""
        course = CourseOut(id=len(self.root) + 1, **course_in.model_dump())
        self.root.append(course)
        return course

    def update(self, course_id: int, course_in: CourseIn) -> CourseOut:
        """Обновить существующий курс по ID."""
        index = next(i for i, course in enumerate(self.root) if course.id == course_id)
        updated = CourseOut(id=course_id, **course_in.model_dump())
        self.root[index] = updated
        return updated

    def delete(self, course_id: int) -> None:
        """Удалить курс по ID."""
        self.root = [course for course in self.root if course.id != course_id]


store = CoursesStore(root=[])


@courses_router.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: int):
    """Получить курс по ID."""
    if not (course := store.find(course_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return course


@courses_router.get("", response_model=list[CourseOut])
async def get_courses():
    """Получить список всех курсов."""
    return store.root


@courses_router.post("", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseIn):
    """Создать новый курс."""
    return store.create(course)


@courses_router.put("/{course_id}", response_model=CourseOut)
async def update_course(course_id: int, course: CourseIn):
    """Обновить курс по ID."""
    if not store.find(course_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return store.update(course_id, course)


@courses_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int):
    """Удалить курс по ID."""
    if not store.find(course_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    store.delete(course_id)


app.include_router(courses_router)
