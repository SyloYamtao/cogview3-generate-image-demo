import os
from typing import Optional

import streamlit as st

import api
from api import generate_chat_scene_prompt, generate_role_appearance, generate_cogview_image
from data_types import ImageMsg, filter_text_msg

st.set_page_config(page_title="CogView API Demo", page_icon="🤖", layout="wide")
debug = os.getenv("DEBUG", "").lower() in ("1", "yes", "y", "true", "t", "on")


def update_api_key(key: Optional[str] = None):
    if debug:
        print(f'update_api_key. st.session_state["API_KEY"] = {st.session_state["API_KEY"]}, key = {key}')
    key = key or st.session_state["API_KEY"]
    if key:
        api.API_KEY = key


def draw_new_image():
    if not verify_meta():
        return
    text_messages = filter_text_msg(st.session_state["history"])
    if text_messages:
        image_prompt = "".join(
            generate_chat_scene_prompt(
                text_messages[-10:],
                meta=st.session_state["meta"]
            )
        )
    else:
        image_prompt = "".join(generate_role_appearance(st.session_state["meta"]["image_prompt"]))

    if not image_prompt:
        st.error("调用chatglm生成Cogview prompt出错")
        return

    image_prompt = f'{st.session_state["IMAGE_STYLE"]}风格。' + image_prompt.strip()

    print(f"image_prompt = {image_prompt}")
    n_retry = 3
    st.markdown("正在生成图片，请稍等...")
    for i in range(n_retry):
        try:
            img_url = generate_cogview_image(image_prompt)
        except Exception as e:
            if i < n_retry - 1:
                st.error("遇到了一点小问题，重试中...")
            else:
                st.error("又失败啦，点击【生成图片】按钮可再次重试")
                return
        else:
            break
    img_msg = ImageMsg({"role": "image", "image": img_url, "caption": image_prompt})
    st.session_state["history"].append(img_msg)
    st.rerun()


api_key = st.sidebar.text_input("API_KEY", value=os.getenv("API_KEY", ""), key="API_KEY", type="password",
                                on_change=update_api_key)
update_api_key(api_key)

st.sidebar.selectbox(label='图片风格：', options=['卡通', '素描', '水墨', '油画', '蜡笔', '哥特', '印象'], index=0,
                     key="IMAGE_STYLE", on_change=draw_new_image)

if "history" not in st.session_state:
    st.session_state["history"] = []
if "meta" not in st.session_state:
    st.session_state["meta"] = {
        "image_prompt": "",
    }


def init_session():
    st.session_state["history"] = []

meta_labels = {
    "image_prompt": "图片的Prompt",
}

with st.container():
    st.text_area(label="图片的Prompt", key="image_prompt",
                 on_change=lambda: st.session_state["meta"].update(image_prompt=st.session_state["image_prompt"]),
                 help="角色的详细人设信息，不可以为空")


def verify_meta() -> bool:
    if st.session_state["meta"]["image_prompt"] == "":
        st.error("生成图片的Prompt不能为空")
        return False
    else:
        return True


button_labels = {
    "clear_meta": "清空Prompt",
    "clear_history": "清空Prompt历史",
    "gen_picture": "生成图片",
}
if debug:
    button_labels.update({
        "show_history": "查看历史"
    })

with st.container():
    n_button = len(button_labels)
    cols = st.columns(n_button)
    button_key_to_col = dict(zip(button_labels.keys(), cols))

    with button_key_to_col["clear_meta"]:
        clear_meta = st.button(button_labels["clear_meta"], key="clear_meta")
        if clear_meta:
            st.session_state["meta"] = {
                "image_prompt": ""
            }
            st.rerun()

    with button_key_to_col["clear_history"]:
        clear_history = st.button(button_labels["clear_history"], key="clear_history")
        if clear_history:
            init_session()
            st.rerun()

    with button_key_to_col["gen_picture"]:
        gen_picture = st.button(button_labels["gen_picture"], key="gen_picture")

    if debug:
        with button_key_to_col["show_history"]:
            show_history = st.button(button_labels["show_history"], key="show_history")
            if show_history:
                print(f"history = {st.session_state['history']}")

for msg in reversed(st.session_state["history"]):
    if msg["role"] == "image":
        with st.chat_message(name="assistant", avatar="assistant"):
            st.image(msg["image"], caption=msg.get("caption", None))
    else:
        raise Exception("Invalid role")

if gen_picture:
    draw_new_image()

with st.chat_message(name="image", avatar="user"):
    input_placeholder = st.empty()
