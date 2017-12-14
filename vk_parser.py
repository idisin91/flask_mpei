import vk_api
def main():
    login, password = '79999643237', 'tyzh_writer'
    vk_session = vk_api.VkApi()
    vk_session.token = 'ab92debfab92debfab92debfbeabce66b9aab92ab92debff2d035dbd851dc3a28075d29'
    # try:
    vk_session.api_login()
    # except vk_api.ApiError as error_msg:
    #     print(error_msg)
    #     return

    vk = vk_session.get_api()

    response = vk.wall.get(count=1)  # Используем метод wall.get

    if response['items']:
        print(response['items'])



if __name__ == "__main__":
    main()