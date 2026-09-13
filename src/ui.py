import customtkinter as ctk

app=ctk.CTk()
app.title("Face attendance system")
app.geometry("1200x700")
app.minsize(1000,600)

# This is the sidebar
sidebar=ctk.CTkFrame(app,width=220)
# ctkframe is a container
sidebar.pack(side="left",fill="y")
# pack - position and layout
# means on the left and y means vertical position


# CTklabel and button are things u put inside container
title=ctk.CTkLabel(
    sidebar,
    text="Face attendance",
    font=("Arial",22,"bold")
)
title.pack(pady=(40,50))

dashboard_button=ctk.CTkButton(
    sidebar,
    text="Dashboard"
)
dashboard_button.pack(pady=10,padx=20,fill="x")

register_button=ctk.CTkButton(
    sidebar,
    text="Register Student"
)

register_button.pack(pady=10,padx=20,fill="x")

attendance_button=ctk.CTkButton(
    sidebar,
    text="Attendance"
)

attendance_button.pack(pady=10,padx=20,fill="x")

main=ctk.CTkFrame(app)
main.pack(side="left",fill="both",expand=True,padx=20,pady=20)
# expand makes the main area take the remaining avaliable space

heading=ctk.CTkLabel(
    main,
    text="Dashboard",
    font=("Arial",28,"bold")
)
heading.pack(anchor="w",padx=20,pady=(10,20))
# padx - horizontal space aroun main , pady-vertical space wjar
content=ctk.CTkFrame(main)
content.pack(fill="both",expand=True,padx=10,pady=10)

camera_panel=ctk.CTkFrame(content)
camera_panel.pack(
    side="left",
    fill="both",
    expand="True",
    padx=(10,5),
    pady=10
)
camera_title=ctk.CTkLabel(
    camera_panel,
    text="Live Camera",
    font=("Arial",20,"bold")
)
camera_title.pack(anchor="w",padx=20,pady=15)

camera_display=ctk.CTkLabel(
    camera_panel,
    text="Camera feed will apear here",
    font=("Arial",18)
)
camera_display.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

attendance_panel=ctk.CTkFrame(content)
attendance_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(5,10),
    pady=10
)

attendance_title=ctk.CTkLabel(
    attendance_panel,
    text="Today's attendance",
    font=("Arial",20,"bold")
)
attendance_title.pack(anchor="w",padx=20,pady=15)

attendance_count=ctk.CTkLabel(
    attendance_panel,
    text="Present: 0",
    font=("Arial",16)
)
attendance_count.pack(anchor="w",padx=20,pady=5)

attendance_list = ctk.CTkTextbox(
    attendance_panel,
    height=400
)
attendance_list.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

attendance_list.insert(
    "end",
    "Student ID         Name       Time\n"
    "--------------------------------------------------------\n"
)

app.mainloop();