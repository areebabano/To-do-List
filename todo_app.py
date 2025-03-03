import streamlit as st
import pandas as pd
import io

# Function to Load Tasks
def load_task():
    try:
        tasks = pd.read_csv("tasks.csv")
        if "Priority" not in tasks.columns:  
            tasks["Priority"] = "Medium 🟠"
        return tasks
    except FileNotFoundError:
        return pd.DataFrame(columns=["Task", "Completed", "Priority"])

# Function to convert DataFrame to CSV for download

def convert_df_to_csv(df):
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

# Function to Save Tasks
def save_task(tasks):
    tasks.to_csv("tasks.csv", index=False)

# Load tasks
tasks = load_task()

# Set up the Streamlit app
st.set_page_config(page_title="To-Do List", page_icon="📝", layout="centered")
st.title("📝 **Interactive To-Do List App** 💗")
st.markdown("📝🌟 **Manage your tasks effortlessly and stay productive!** 🚀 Organize, prioritize, and achieve your goals🌠 with ease.✔😊")

# Sidebar: Add New Task
st.sidebar.header("➕ Add New Task")
new_task = st.sidebar.text_input("Enter a new task:")
priority = st.sidebar.radio("Set priority:", ["High 🔴", "Medium 🟠", "Low 🟢"], horizontal=True)

if st.sidebar.button("➕ Add Task", use_container_width=True):
    if new_task:
        new_row = pd.DataFrame([{"Task": new_task, "Completed": False, "Priority": priority}])
        tasks = pd.concat([tasks, new_row], ignore_index=True)
        save_task(tasks)
        st.rerun()
    else:
        st.sidebar.warning("⚠️ Please enter a task before adding.")

# Sidebar: Update Task
st.sidebar.header("✏️ Update Task")
if not tasks.empty:
    task_to_update = st.sidebar.selectbox("Select a task:", tasks["Task"].tolist())
    updated_task = st.sidebar.text_input("Update task:")
    updated_priority = st.sidebar.radio("Update priority:", ["High 🔴", "Medium 🟠", "Low 🟢"], horizontal=True)
    
    if st.sidebar.button("✏️ Update Task", use_container_width=True):
        tasks.loc[tasks["Task"] == task_to_update, ["Task", "Priority"]] = [updated_task, updated_priority]
        save_task(tasks)
        st.rerun()
    

# Sidebar: Download CSV Button
st.sidebar.header("📥 Download Tasks")
if not tasks.empty:
    csv_data = convert_df_to_csv(tasks)
    st.sidebar.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name="tasks.csv",
        mime="text/csv",
        use_container_width=True
    )

# Task Progress
if not tasks.empty:
    completed_tasks = tasks["Completed"].sum()
    total_tasks = len(tasks)
    progress = completed_tasks / total_tasks if total_tasks > 0 else 0

    st.progress(progress)
    st.write(f"✅ **Completed: {completed_tasks} / {total_tasks}**")

# Display Pending Tasks
st.subheader("⏳ **Pending Tasks**")
pending_tasks = tasks[tasks["Completed"] == False]
if not pending_tasks.empty:
    for index, row in pending_tasks.iterrows():
        with st.expander(f"📝 {row['Task']} ({row['Priority']})", expanded=False):
            col1, col2 = st.columns([5, 1])

            if col1.checkbox("☑ Mark as Done", row["Completed"], key=index):
                tasks.at[index, "Completed"] = True
                save_task(tasks)
                st.rerun()

            if col2.button("✖ Delete", key=f"delete_{index}"):
                tasks = tasks.drop(index).reset_index(drop=True)
                save_task(tasks)
                st.rerun()
else:
    st.info("🎉 No pending tasks! You're all caught up.")

# Display Completed Tasks
st.subheader("✅ **Completed Tasks**")
completed_tasks = tasks[tasks["Completed"] == True]
if not completed_tasks.empty:
    for index, row in completed_tasks.iterrows():
        with st.expander(f"✅ {row['Task']} ({row['Priority']})", expanded=False):
            col1, col2 = st.columns([5, 1])

            if col2.button("✖ Delete", key=f"delete_done_{index}"):
                tasks = tasks.drop(index).reset_index(drop=True)
                save_task(tasks)
                st.rerun()
else:
    st.info("⏳ No completed tasks yet! Keep going! 🚀")

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🚀 **Built with Streamlit | Created by Areeba Hammad 💗**")


# import streamlit as st
# import pandas as pd

# def load_task():
#   try:
#     return pd.read_csv("tasks.csv")
#   except FileNotFoundError:
#     return pd.DataFrame(columns=["Task", "Completed"])

# def save_task(tasks):
#   tasks.to_csv("tasks.csv", index=False)

# tasks = load_task()

# # To-do List app 

# st.set_page_config(page_title = "To-Do List", page_icon = "📝", layout = "centered")
# st.title("📝---------To-Do List App---------💗")
# st.markdown("😊 Stay organized and track your tasks easily! 🌟")

# # Add Task 

# st.sidebar.header("➕ Add New Task")
# new_task = st.sidebar.text_input("Enter a new task: ")
# if st.sidebar.button("Add Task ✔", use_container_width=True):
#   if new_task:
#     new_row = pd.DataFrame([{"Task": new_task, "Completed": False}])  
#     tasks = pd.concat([tasks, new_row], ignore_index=True) 
#     save_task(tasks)
#     st.rerun()
#     st.success("Task added successfully! 😊✔")
#   else:
#     st.sidebar.warning("⚠️ Please enter a task before adding.")
  
# # Update Task

# st.sidebar.header("✏️ Update Task")
# if not tasks.empty:
#   task_to_update = st.sidebar.selectbox("Select a task to update:", tasks["Task"].tolist())
#   updated_task = st.sidebar.text_input("➕ Add a new updated task: ")
#   if st.sidebar.button("Updated Task ✔", use_container_width=True):
#     tasks.loc[tasks["Task"] == task_to_update , "Task"] = updated_task
#     save_task(tasks)
#     st.rerun()
#     st.success("Task updated successfully! 😊✔")

# # Show Task List

# st.subheader("📌 Your Tasks List")
# if not tasks.empty:
#   for index, row in tasks.iterrows():
#     col1, col2, col3 = st.columns([5, 1, 1])
#     col1.write(f"📝 {row['Task']}")
#     if col2.checkbox("☑ Done", row["Completed"], key=index):
#       tasks.at[index, "Completed"] = not row["Completed"]
#       save_task(tasks)
#       st.rerun()
#     if col3.button("✖ Delete", key=f"delete_{index}"):
#       tasks = tasks.drop(index).reset_index(drop=True)
#       save_task(tasks)
#       st.rerun()
#       st.success("Task deleted ✖ successfully! 😊✔")
# else: 
#   st.info("No tasks added yet! ✖ use the sidebar to add new task 😊📝.")
  

# st.sidebar.markdown("---")
# st.sidebar.markdown("🚀🌟 Built with Streamlit | Created by Areeba Hammad 💗")