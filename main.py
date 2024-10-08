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


# Streamlit aplikacija
st.title("Vježbanje konverzije cilindričnih leća")

# Opcija za izbor tipa vježbe
exercise_type = st.radio(
    "Odaberite vrstu vježbe:",
    ("Standardna konverzija", "Konverzija ukrštenih cilindara"),
)


# Funkcija za unos korisničkih odgovora za standardnu konverziju
def standard_conversion_input():
    cols = st.columns(3)
    with cols[0]:
        user_dsph = st.number_input("Novi dsph", value=None, step=0.25, format="%.2f")
    with cols[1]:
        user_dcyl = st.number_input("Novi dcyl", value=None, step=0.25, format="%.2f")
    with cols[2]:
        user_axis = st.number_input("Nova os", value=None, min_value=0, max_value=180, step=1, format="%d")
    return user_dsph, user_dcyl, user_axis


# Funkcija za unos korisničkih odgovora za ukrštene cilindre
def cross_cylinder_input():
    st.write("Rješenje 1:")
    cols1 = st.columns(3)
    with cols1[0]:
        user_dsph1 = st.number_input("Novi dsph (Rješenje 1)", value=None, step=0.25, format="%.2f", key='user_dsph1')
    with cols1[1]:
        user_dcyl1 = st.number_input("Novi dcyl (Rješenje 1)", value=None, step=0.25, format="%.2f", key='user_dcyl1')
    with cols1[2]:
        user_axis1 = st.number_input(
            "Nova os (Rješenje 1)", value=None, min_value=0, max_value=180, step=1, format="%d", key='user_axis1'
            )
    
    st.write("Rješenje 2:")
    cols2 = st.columns(3)
    with cols2[0]:
        user_dsph2 = st.number_input("Novi dsph (Rješenje 2)", value=None, step=0.25, format="%.2f", key='user_dsph2')
    with cols2[1]:
        user_dcyl2 = st.number_input("Novi dcyl (Rješenje 2)", value=None, step=0.25, format="%.2f", key='user_dcyl2')
    with cols2[2]:
        user_axis2 = st.number_input(
            "Nova os (Rješenje 2)", value=None, min_value=0, max_value=180, step=1, format="%d", key='user_axis2'
            )
    
    return (user_dsph1, user_dcyl1, user_axis1), (user_dsph2, user_dcyl2, user_axis2)


# Zamjena postojeće funkcionalnosti unosa u glavnoj aplikaciji
if exercise_type == "Standardna konverzija":
    if 'standard_task' not in st.session_state:
        st.session_state.standard_task = generate_standard_task()
    
    dsph, dcyl, axis = st.session_state.standard_task
    
    st.write(f"Konvertirajte sljedeći recept za leće:")
    st.write(f"Dsph: {dsph:+} | Dcyl: {dcyl:+} | Os: {axis}°")
    
    user_dsph, user_dcyl, user_axis = standard_conversion_input()
    
    if st.button("Provjeri odgovor"):
        correct_dsph, correct_dcyl, correct_axis = convert_standard_cylinder(dsph, dcyl, axis)
        if check_answer(user_dsph, user_dcyl, user_axis, correct_dsph, correct_dcyl, correct_axis):
            st.success("Točno!")
        else:
            st.error(f"Netočno. Točan odgovor je Dsph: {correct_dsph:+}, Dcyl: {correct_dcyl:+}, Os: {correct_axis}°")
    
    if st.button("Generiraj novi zadatak"):
        st.session_state.standard_task = generate_standard_task()
        st.rerun()

else:
    if 'cross_cylinder_task' not in st.session_state:
        st.session_state.cross_cylinder_task = generate_cross_cylinder_task()
    
    dcyl1, axis1, dcyl2, axis2 = st.session_state.cross_cylinder_task
    
    st.write(f"Konvertirajte sljedeći recept za ukrštene cilindre:")
    st.write(f"Dcyl1: {dcyl1:+} ax {axis1}° | Dcyl2: {dcyl2:+} ax {axis2}°")
    
    (user_dsph1, user_dcyl1, user_axis1), (user_dsph2, user_dcyl2, user_axis2) = cross_cylinder_input()
    
    if st.button("Provjeri odgovor"):
        (correct_dsph1, correct_dcyl1, correct_axis1), (
        correct_dsph2, correct_dcyl2, correct_axis2) = convert_cross_cylinder(dcyl1, axis1, dcyl2, axis2)
        
        correct_1 = check_answer(user_dsph1, user_dcyl1, user_axis1, correct_dsph1, correct_dcyl1, correct_axis1)
        correct_2 = check_answer(user_dsph2, user_dcyl2, user_axis2, correct_dsph2, correct_dcyl2, correct_axis2)
        
        correct_3 = check_answer(user_dsph1, user_dcyl1, user_axis1, correct_dsph2, correct_dcyl2, correct_axis2)
        correct_4 = check_answer(user_dsph2, user_dcyl2, user_axis2, correct_dsph1, correct_dcyl1, correct_axis1)
        
        if correct_1 or correct_4:
            st.success("Rješenje 1 je točno!")
        else:
            st.error(
                f"Rješenje 1 je netočno. Točan odgovor može biti Dsph: {correct_dsph1:+}, Dcyl: {correct_dcyl1:+}, Os: {correct_axis1}° ili Dsph: {correct_dsph2:+}, Dcyl: {correct_dcyl2:+}, Os: {correct_axis2}°"
                )
        
        if correct_2 or correct_3:
            st.success("Rješenje 2 je točno!")
        else:
            st.error(
                f"Rješenje 2 je netočno. Točan odgovor može biti Dsph: {correct_dsph1:+}, Dcyl: {correct_dcyl1:+}, Os: {correct_axis1}° ili Dsph: {correct_dsph2:+}, Dcyl: {correct_dcyl2:+}, Os: {correct_axis2}°"
                )
    
    if st.button("Generiraj novi zadatak"):
        st.session_state.cross_cylinder_task = generate_cross_cylinder_task()
        st.rerun()
