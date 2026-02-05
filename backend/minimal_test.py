from sqlmodel import SQLModel, Field

# Minimal test
class TaskBase(SQLModel):
    title: str = Field(min_length=1)

class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: int = Field(default=None, primary_key=True)

print("Minimal model created successfully!")