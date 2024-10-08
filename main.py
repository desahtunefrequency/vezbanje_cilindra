import streamlit as st
import random


# Funkcija za generiranje zadatka za standardnu konverziju
def generate_standard_task():
    dsph = round(random.uniform(-6.00, +6.00) / 0.25) * 0.25
    dcyl = round(random.uniform(-4.00, +4.00) / 0.25) * 0.25
    axis = random.randint(0, 180)
    return dsph, dcyl, axis


# Funkcija za generiranje zadatka za ukrštene cilindre
def generate_cross_cylinder_task():
    dcyl1 = round(random.uniform(-4.00, +4.00) / 0.25) * 0.25
    axis1 = random.randint(0, 180)
    dcyl2 = round(random.uniform(-4.00, +4.00) / 0.25) * 0.25
    axis2 = (axis1 + 90) % 180
    return dcyl1, axis1, dcyl2, axis2


# Funkcija za konverziju cilindara
def convert_standard_cylinder(dsph, dcyl, axis):
    new_dsph = dsph + dcyl
    new_dcyl = -dcyl
    new_axis = (axis + 90) % 180
    return new_dsph, new_dcyl, new_axis


# Funkcija za konverziju ukrštenih cilindara
def convert_cross_cylinder(dcyl1, axis1, dcyl2, axis2):
    if abs(axis1 - axis2) % 180 != 90:
        raise ValueError("Axes must be 90 degrees apart")

    dsph_1 = min(dcyl1, dcyl2)
    dcyl_1 = abs(dcyl1 - dcyl2)
    axis_1 = axis2 if dcyl1 < dcyl2 else axis1

    dsph_2 = max(dcyl1, dcyl2)
    dcyl_2 = -abs(dcyl1 - dcyl2)
    axis_2 = axis1 if dcyl1 < dcyl2 else axis2

    return (dsph_1, dcyl_1, axis_1), (dsph_2, dcyl_2, axis_2)


# Funkcija za provjeru točnosti odgovora
def check_answer(
    user_dsph, user_dcyl, user_axis, correct_dsph, correct_dcyl, correct_axis
):
    return (
        round(user_dsph, 2) == round(correct_dsph, 2)
        and round(user_dcyl, 2) == round(correct_dcyl, 2)
        and round(user_axis, 2) == round(correct_axis, 2)
    )


# Streamlit app title
st.title("Vježbanje konverzije cilindričnih leća")

# Select type of exercise
exercise_type = st.radio(
    "Odaberite vrstu vježbe:",
    ("Standardna konverzija", "Konverzija ukrštenih cilindara"),
)

# Main app logic for "Standardna konverzija"
if exercise_type == "Standardna konverzija":
    if 'standard_task' not in st.session_state:
        st.session_state.standard_task = generate_standard_task()

    dsph, dcyl, axis = st.session_state.standard_task

    st.write(f"Konvertirajte sljedeći recept za leće:")
    st.write(f"Dsph: {dsph:+} | Dcyl: {dcyl:+} | Os: {axis}°")

    # Initialize user inputs in session state if they are not already present
    if 'user_dsph' not in st.session_state:
        st.session_state.user_dsph = 0
    if 'user_dcyl' not in st.session_state:
        st.session_state.user_dcyl = 0
    if 'user_axis' not in st.session_state:
        st.session_state.user_axis = 0

    # User input fields
    st.session_state.user_dsph = st.number_input("Novi dsph", value=st.session_state.user_dsph, step=0.25, format="%.2f")
    st.session_state.user_dcyl = st.number_input("Novi dcyl", value=st.session_state.user_dcyl, step=0.25, format="%.2f")
    st.session_state.user_axis = st.number_input("Nova os", value=st.session_state.user_axis, min_value=0, max_value=180, step=1, format="%d")

    # Check answer button
    if st.button("Provjeri odgovor"):
        correct_dsph, correct_dcyl, correct_axis = convert_standard_cylinder(dsph, dcyl, axis)
        if check_answer(st.session_state.user_dsph, st.session_state.user_dcyl, st.session_state.user_axis, correct_dsph, correct_dcyl, correct_axis):
            st.success("Točno!")
        else:
            st.error(f"Netočno. Točan odgovor je Dsph: {correct_dsph:+}, Dcyl: {correct_dcyl:+}, Os: {correct_axis}°")

    # Generate new task button
    if st.button("Generiraj novi zadatak"):
        st.session_state.standard_task = generate_standard_task()
        st.session_state.user_dsph = 0
        st.session_state.user_dcyl = 0
        st.session_state.user_axis = 0
        st.rerun()

# Main app logic for "Konverzija ukrštenih cilindara"
else:
    if 'cross_cylinder_task' not in st.session_state:
        st.session_state.cross_cylinder_task = generate_cross_cylinder_task()

    dcyl1, axis1, dcyl2, axis2 = st.session_state.cross_cylinder_task

    st.write(f"Konvertirajte sljedeći recept za ukrštene cilindre:")
    st.write(f"Dcyl1: {dcyl1:+} ax {axis1}° | Dcyl2: {dcyl2:+} ax {axis2}°")

    # Initialize user inputs in session state if they are not already present
    if 'user_dsph1' not in st.session_state:
        st.session_state.user_dsph1 = 0
    if 'user_dcyl1' not in st.session_state:
        st.session_state.user_dcyl1 = 0
    if 'user_axis1' not in st.session_state:
        st.session_state.user_axis1 = 0
    if 'user_dsph2' not in st.session_state:
        st.session_state.user_dsph2 = 0
    if 'user_dcyl2' not in st.session_state:
        st.session_state.user_dcyl2 = 0
    if 'user_axis2' not in st.session_state:
        st.session_state.user_axis2 = 0

    # User input fields
    st.session_state.user_dsph1 = st.number_input("Novi dsph (Rješenje 1)", value=st.session_state.user_dsph1, step=0.25, format="%.2f", key='user_dsph1')
    st.session_state.user_dcyl1 = st.number_input("Novi dcyl (Rješenje 1)", value=st.session_state.user_dcyl1, step=0.25, format="%.2f", key='user_dcyl1')
    st.session_state.user_axis1 = st.number_input("Nova os (Rješenje 1)", value=st.session_state.user_axis1, min_value=0, max_value=180, step=1, format="%d", key='user_axis1')

    st.session_state.user_dsph2 = st.number_input("Novi dsph (Rješenje 2)", value=st.session_state.user_dsph2, step=0.25, format="%.2f", key='user_dsph2')
    st.session_state.user_dcyl2 = st.number_input("Novi dcyl (Rješenje 2)", value=st.session_state.user_dcyl2, step=0.25, format="%.2f", key='user_dcyl2')
    st.session_state.user_axis2 = st.number_input("Nova os (Rješenje 2)", value=st.session_state.user_axis2, min_value=0, max_value=180, step=1, format="%d", key='user_axis2')

    # Check answer button
    if st.button("Provjeri odgovor"):
        (correct_dsph1, correct_dcyl1, correct_axis1), (correct_dsph2, correct_dcyl2, correct_axis2) = convert_cross_cylinder(dcyl1, axis1, dcyl2, axis2)

        correct_1 = check_answer(st.session_state.user_dsph1, st.session_state.user_dcyl1, st.session_state.user_axis1, correct_dsph1, correct_dcyl1, correct_axis1)
        correct_2 = check_answer(st.session_state.user_dsph2, st.session_state.user_dcyl2, st.session_state.user_axis2, correct_dsph2, correct_dcyl2, correct_axis2)

        correct_3 = check_answer(st.session_state.user_dsph1, st.session_state.user_dcyl1, st.session_state.user_axis1, correct_dsph2, correct_dcyl2, correct_axis2)
        correct_4 = check_answer(st.session_state.user_dsph2, st.session_state.user_dcyl2, st.session_state.user_axis2, correct_dsph1, correct_dcyl1, correct_axis1)

        if correct_1 or correct_4:
            st.success("Rješenje 1 je točno!")
        else:
            st.error(f"Rješenje 1 je netočno. Točan odgovor može biti Dsph: {correct_dsph1:+}, Dcyl: {correct_dcyl1:+}, Os: {correct_axis1}° ili Dsph: {correct_dsph2:+}, Dcyl: {correct_dcyl2:+}, Os: {correct_axis2}°")

        if correct_2 or correct_3:
            st.success("Rješenje 2 je točno!")
        else:
            st.error(f"Rješenje 2 je netočno. Točan odgovor može biti Dsph: {correct_dsph1:+}, Dcyl: {correct_dcyl1:+}, Os: {correct_axis1}° ili Dsph: {correct_dsph2:+}, Dcyl: {correct_dcyl2:+}, Os: {correct_axis2}°")

    # Generate new task button
    if st.button("Generiraj novi zadatak"):
        st.session_state.cross_cylinder_task = generate_cross_cylinder_task()
        st.session_state.user_dsph1 = 0
        st.session_state.user_dcyl1 = 0
        st.session_state.user_axis1 = 0
        st.session_state.user_dsph2 = 0
        st.session_state.user_dcyl2 = 0
        st.session_state.user_axis2 = 0
        st.rerun()
