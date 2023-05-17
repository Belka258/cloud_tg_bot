from os import name
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

import Token
from VPC.VPC import *
from ECS.ECS import *
from EVS.EVS import *
from RDS.RDS import *
from IMS.IMS import *

bot = Bot(Token.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

user_data = None

start_mess = 'Добрый день, войдите в аккаунт, для этого введите команду /login'

keyboard_choose = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_show = types.KeyboardButton('Вывести')
button_create = types.KeyboardButton('Создать')
button_delete = types.KeyboardButton('Удалить')
button_modify = types.KeyboardButton('Редактировать')
keyboard_choose.add(button_show, button_create, button_delete, button_modify)

keyboard_show = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_show_VPC = types.KeyboardButton('Вывести VPC')
button_show_VPC_sub = types.KeyboardButton('Вывести VPC Subnet')
button_show_ECS = types.KeyboardButton('Вывести ECS')
button_show_EVS = types.KeyboardButton('Вывести EVS')
button_show_RDS = types.KeyboardButton('Вывести RDS')
button_menu = types.KeyboardButton('Меню')
keyboard_show.add(button_show_VPC, button_show_VPC_sub, button_show_ECS, button_show_EVS, button_show_RDS, button_menu)

keyboard_what_delete = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_delete_vpc = types.KeyboardButton('Удалить VPC')
button_delete_vpc_sub = types.KeyboardButton('Удалить VPC Subnet')
button_delete_evs = types.KeyboardButton('Удалить EVS')
button_delete_ecs = types.KeyboardButton('Удалить ECS')
button_delete_rds = types.KeyboardButton('Удалить RDS')
keyboard_what_delete.add(button_delete_vpc, button_delete_vpc_sub, button_delete_evs, button_delete_ecs,
                         button_delete_rds)

keyboard_what_create = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_create_vpc = types.KeyboardButton('Создать VPC')
button_create_vpc_sub = types.KeyboardButton('Создать VPC Subnet')
button_create_evs = types.KeyboardButton('Создать EVS')
keyboard_what_create.add(button_create_vpc, button_create_vpc_sub, button_create_evs)

keyboard_what_modify = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_modify_vpc = types.KeyboardButton('Редактировать VPC')
button_modify_vpc_sub = types.KeyboardButton('Редактировать VPC Subnet')
button_modify_evs = types.KeyboardButton('Редактировать EVS')
button_modify_ecs = types.KeyboardButton('Редактировать ECS')
button_modify_rds = types.KeyboardButton('Редактировать RDS')
keyboard_what_modify.add(button_modify_vpc, button_modify_vpc_sub, button_modify_evs, button_modify_ecs,
                         button_modify_rds)

keyboard_modify_evs = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_modify_evs_n = types.KeyboardButton('Изменить имя EVS')
button_modify_evs_s = types.KeyboardButton('Изменить размер EVS')
keyboard_modify_evs.add(button_modify_evs_n, button_modify_evs_s)

keyboard_modify_vpc = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_modify_vpc_n = types.KeyboardButton('Изменить имя VPC')
keyboard_modify_vpc.add(button_modify_vpc_n)

keyboard_modify_vpc_sub = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_modify_vpc_sub_n = types.KeyboardButton('Изменить имя VPC Subnet')
keyboard_modify_vpc_sub.add(button_modify_vpc_sub_n)

keyboard_modify_ecs = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_modify_ecs_n = types.KeyboardButton('Изменить имя ECS')
keyboard_modify_ecs.add(button_modify_ecs_n)

keyboard_modify_rds = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_modify_rds_n = types.KeyboardButton('Изменить имя RDS')
keyboard_modify_rds.add(button_modify_rds_n)


class Login(StatesGroup):
    access_Key_Id = State()
    secret_Access_Key = State()
    project_ID = State()


class Name(StatesGroup):
    typE = State()
    name = State()


class VPC_creation_info(StatesGroup):
    cidr = State()
    name = State()


class VPC_subnet_creation_info(StatesGroup):
    name = State()
    cidr = State()
    vpc_name = State()
    gateway_ip = State()
    ipv6 = State()


class EVS_creation_info(StatesGroup):
    name = State()
    disk_type = State()
    size = State()
    count = State()
    az = State()


class EVS_change_size(StatesGroup):
    name = State()
    size = State()


class Change_name(StatesGroup):
    name = State()
    new_name = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(text=start_mess)


@dp.message_handler(commands=['login'])
async def cmd_login(message: types.Message):
    await Login.access_Key_Id.set()
    await message.answer("Введите Access Key ID")


@dp.message_handler(state=Login.access_Key_Id)
async def process_access_key(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['access_Key_Id'] = message.text
    await Login.next()
    await message.answer("Введите Secret Access Key")


@dp.message_handler(state=Login.secret_Access_Key)
async def process_secret_access_key(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['secret_Access_Key'] = message.text
    await Login.next()
    await message.answer("Введите Project ID")


@dp.message_handler(state=Login.project_ID)
async def process_project_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['project_ID'] = message.text
        global user_data
        user_data = data
    await state.finish()
    await message.answer('Что делаем?', reply_markup=keyboard_choose)


@dp.message_handler(lambda message: message.text == "Меню")
async def menu(message: types.Message):
    await message.answer('Что делаем?', reply_markup=keyboard_choose)


###################################################################################


@dp.message_handler(lambda message: message.text == 'Вывести')
async def print_(message: types.Message):
    await message.answer('Что вывести?', reply_markup=keyboard_show)


@dp.message_handler(lambda message: message.text == "Вывести VPC")
async def VPC_print(message: types.Message):
    vpc = VPC(user_data['access_Key_Id'], user_data['secret_Access_Key'], user_data['project_ID']).get_json_of_vpc()
    for i in range(len(vpc)):
        await bot.send_message(message.chat.id, text=f'name = {vpc[i].name}\n'
                                                     f'cidr = {vpc[i].cidr}\n'
                                                     f'status = {vpc[i].status}\n'
                                                     f'id = {vpc[i].id}')


@dp.message_handler(lambda message: message.text == "Вывести VPC Subnet")
async def VPC_sub_print(message: types.Message):
    vpc = VPC(user_data['access_Key_Id'], user_data['secret_Access_Key'], user_data['project_ID']).get_json_of_subnets()
    for i in range(len(vpc)):
        await bot.send_message(message.chat.id, text=f'name = {vpc[i].name}\n'
                                                     f'cidr = {vpc[i].cidr}\n'
                                                     f'status = {vpc[i].status}\n'
                                                     f'gateway ip = {vpc[i].gateway_ip}')


@dp.message_handler(lambda message: message.text == "Вывести ECS")
async def ECS_print(message: types.Message):
    d = ECS(user_data['access_Key_Id'], user_data['secret_Access_Key'], user_data['project_ID']).get_json_of_ecs()
    for i in range(len(d)):
        await bot.send_message(message.chat.id, text=f'name = {d[i].name}\n'
                                                     f'status = {d[i].status}\n'
                                                     f'os type = {d[i].metadata["os_type"]}\n'
                                                     f'image name = {d[i].metadata["image_name"]}\n'
                                                     f'os ram = {d[i].flavor.ram}\n'
                                                     f'os vcpus = {d[i].flavor.vcpus}\n')


@dp.message_handler(lambda message: message.text == "Вывести EVS")
async def EVS_print(message: types.Message):
    e = EVS(user_data['access_Key_Id'], user_data['secret_Access_Key'], user_data['project_ID']).get_json_of_evs()
    for i in range(len(e)):
        await bot.send_message(message.chat.id, text=f'name = {e[i].name}\n'
                                                     f'status = {e[i].status}\n'
                                                     f'os type = {e[i].volume_type}\n'
                                                     f'image size = {e[i].size}\n'
                                                     f'zone = {e[i].availability_zone}\n')


@dp.message_handler(lambda message: message.text == "Вывести RDS")
async def VPC_print(message: types.Message):
    rds = RDS(user_data['access_Key_Id'], user_data['secret_Access_Key'], user_data['project_ID']).get_json_of_rds()
    for i in range(len(rds)):
        await bot.send_message(message.chat.id, text=f'name = {rds[i].name}\n'
                                                     f'status = {rds[i].status}\n'
                                                     f'database = {rds[i].datastore.type} {rds[i].datastore.version}\n'
                                                     f'flavor ref = {rds[i].flavor_ref}\n'
                                                     f'cpu mem = {rds[i].cpu} {rds[i].mem}\n'
                                                     f'volume = {rds[i].volume.type} {rds[i].volume.size}\n')


###################################################################################


@dp.message_handler(lambda message: message.text == 'Создать')
async def create(message: types.Message):
    await message.answer('Что создаем?', reply_markup=keyboard_what_create)


@dp.message_handler(lambda message: message.text == 'Создать VPC')
async def create_vpc(message: types.Message):
    await VPC_creation_info.cidr.set()
    await message.answer('введите CIDR')

    @dp.message_handler(state=VPC_creation_info.cidr)
    async def process_vpc_cidr(message: types.Message, state: FSMContext):
        async with state.proxy() as vpc_create:
            vpc_create['cidr'] = message.text
        await VPC_creation_info.next()
        await message.answer("Введите имя")

    @dp.message_handler(state=VPC_creation_info.name)
    async def process_vpc_name(message: types.Message, state: FSMContext):
        async with state.proxy() as vpc_create:
            vpc_create['name'] = message.text
            global user_data
            vpc = VPC(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                      user_data['project_ID']).create_new_vpc(vpc_create['cidr'], vpc_create['name'])
        await state.finish()
        await message.answer('VPC создана', reply_markup=keyboard_choose)


@dp.message_handler(lambda message: message.text == 'Создать VPC Subnet')
async def create_vpc_sub(message: types.Message):
    await VPC_subnet_creation_info.name.set()
    await message.answer('Введите имя')

    @dp.message_handler(state=VPC_subnet_creation_info.name)
    async def process_vpc_sub_name(message: types.Message, state: FSMContext):
        async with state.proxy() as vpc_sub_create:
            vpc_sub_create['name'] = message.text
        await VPC_subnet_creation_info.next()
        await message.answer("Введите CIDR")

    @dp.message_handler(state=VPC_subnet_creation_info.cidr)
    async def process_vpc_sub_cidr(message: types.Message, state: FSMContext):
        async with state.proxy() as vpc_sub_create:
            vpc_sub_create['cidr'] = message.text
        await VPC_subnet_creation_info.next()
        await message.answer("Введите имя VPC")

    @dp.message_handler(state=VPC_subnet_creation_info.vpc_name)
    async def process_vpc_sub_vpc_name(message: types.Message, state: FSMContext):
        async with state.proxy() as vpc_sub_create:
            vpc_sub_create['vpc_name'] = message.text
        await VPC_subnet_creation_info.next()
        await message.answer("Введите IP")

    @dp.message_handler(state=VPC_subnet_creation_info.gateway_ip)
    async def process_vpc_sub_gateway_ip(message: types.Message, state: FSMContext):
        async with state.proxy() as vpc_sub_create:
            vpc_sub_create['gateway_ip'] = message.text
        await VPC_subnet_creation_info.next()
        await message.answer("Введите IPV6")

    @dp.message_handler(state=VPC_subnet_creation_info.ipv6)
    async def process_vpc_sub_name(message: types.Message, state: FSMContext):
        async with state.proxy() as vpc_sub_create:
            vpc_sub_create['ipv6'] = message.text
            global user_data
            vpc_s = VPC(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                        user_data['project_ID']).create_new_subnet(vpc_sub_create['name'], vpc_sub_create['cidr'],
                                                                   vpc_sub_create['vpc_name'],
                                                                   vpc_sub_create['gateway_ip'],
                                                                   vpc_sub_create['ipv6'])
        await state.finish()
        await message.answer('VPC Subnet создана', reply_markup=keyboard_choose)


@dp.message_handler(lambda message: message.text == 'Создать EVS')
async def create_vpc_sub(message: types.Message):
    await EVS_creation_info.name.set()
    await message.answer('Введите имя')

    @dp.message_handler(state=EVS_creation_info.name)
    async def process_ecs_name(message: types.Message, state: FSMContext):
        async with state.proxy() as evs_create:
            evs_create['name'] = message.text
        await EVS_creation_info.next()
        await message.answer("Введите тип EVS")

    @dp.message_handler(state=EVS_creation_info.disk_type)
    async def process_ecs_disk_type(message: types.Message, state: FSMContext):
        async with state.proxy() as evs_create:
            evs_create['disk_type'] = message.text
        await EVS_creation_info.next()
        await message.answer("Введите размер")

    @dp.message_handler(state=EVS_creation_info.size)
    async def process_ecs_size(message: types.Message, state: FSMContext):
        async with state.proxy() as evs_create:
            evs_create['size'] = message.text
        await EVS_creation_info.next()
        await message.answer("Введите количество")

    @dp.message_handler(state=EVS_creation_info.count)
    async def process_ecs_count(message: types.Message, state: FSMContext):
        async with state.proxy() as evs_create:
            evs_create['count'] = message.text
        await EVS_creation_info.next()
        await message.answer("Введите зону доступности")

    @dp.message_handler(state=EVS_creation_info.az)
    async def process_ecs_az(message: types.Message, state: FSMContext):
        async with state.proxy() as evs_create:
            evs_create['az'] = message.text
            global user_data
            evs = VPC(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                      user_data['project_ID']).create_new_evs(evs_create['name'], evs_create['disk_type'],
                                                              int(evs_create['size']), int(evs_create['count']),
                                                              evs_create['az'])
        await state.finish()
        await message.answer('EVS создана', reply_markup=keyboard_choose)


###################################################################################


@dp.message_handler(lambda message: message.text == 'Удалить')
async def delete(message: types.Message):
    await message.answer('Что удаляем?', reply_markup=keyboard_what_delete)


@dp.message_handler(lambda message: message.text == 'Удалить VPC' or message.text == 'Удалить VPC Subnet'
                                    or message.text == 'Удалить EVS')
async def delete_vpc(message: types.Message, state: FSMContext):
    await message.answer('Введите название')
    await Name.typE.set()
    async with state.proxy() as deletE:
        deletE['typE'] = message.text
    await Name.next()


@dp.message_handler(state=Name.name)
async def delete_vpc_via_name(message: types.Message, state: FSMContext):
    async with state.proxy() as deletE:
        deletE['name'] = message.text
        global user_data
        if deletE['typE'] == 'Удалить VPC':
            VPC(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                user_data['project_ID']).delete_vpc_by_name(deletE['name'])
            await message.answer('vpc удалена', reply_markup=keyboard_choose)
        elif deletE['typE'] == 'Удалить VPC Subnet':
            VPC(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                user_data['project_ID']).delete_subnet_from_vpc(deletE['name'])
            await message.answer('VPC Subnet удалена', reply_markup=keyboard_choose)
        elif deletE['typE'] == 'Удалить EVS':
            EVS(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                user_data['project_ID']).delete_evs_by_name(deletE['name'])
            await message.answer('EVS удалена', reply_markup=keyboard_choose)
        elif deletE['typE'] == 'Удалить ECS':
            ECS(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                user_data['project_ID']).delete_ecs_by_name(deletE['name'])
            await message.answer('ECS удалена', reply_markup=keyboard_choose)
        elif deletE['typE'] == 'Удалить RDS':
            RDS(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                user_data['project_ID']).delete_rds_by_name(deletE['name'])
            await message.answer('RDS удалена', reply_markup=keyboard_choose)

    await state.finish()


###################################################################################


@dp.message_handler(lambda message: message.text == 'Редактировать')
async def modify(message: types.Message):
    await message.answer('Что редактируем?', reply_markup=keyboard_what_modify)


@dp.message_handler(lambda message: message.text == 'Редактировать EVS')
async def modify_evs(message: types.Message):
    await message.answer('Что редактируем?', reply_markup=keyboard_modify_evs)

    @dp.message_handler(lambda message: message.text == 'Изменить размер EVS')
    async def modify_evs_c(message: types.Message):
        await EVS_change_size.name.set()
        await message.answer('Введите имя EVS')

        @dp.message_handler(state=EVS_change_size.name)
        async def process_evs_name_ch(message: types.Message, state: FSMContext):
            async with state.proxy() as EVS_ch_s:
                EVS_ch_s['name'] = message.text
            await EVS_change_size.name.next()
            await message.answer('Введите новый размер EVS')

        @dp.message_handler(state=EVS_change_size.size)
        async def process_evs_size_ch(message: types.Message, state: FSMContext):
            async with state.proxy() as EVS_ch_s:
                EVS_ch_s['size'] = message.text
                ch_s_evs = EVS(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                               user_data['project_ID']).expand_disk_by_name(EVS_ch_s['name'], EVS_ch_s['size'])
            await state.finish()
            await message.answer('Размер EVS изменен', reply_markup=keyboard_choose)

        @dp.message_handler(lambda message: message.text == 'Изменить имя EVS')
        async def modify_evs_n(message: types.Message):
            await Change_name.name.set()
            await message.answer('Введите старое имя EVS')

            @dp.message_handler(state=Change_name.name)
            async def process_evs_name_ch(message: types.Message, state: FSMContext):
                async with state.proxy() as EVS_ch_n:
                    EVS_ch_n['name'] = message.text
                await Change_name.name.next()
                await message.answer('Введите новое имя EVS')

            @dp.message_handler(state=Change_name.new_name)
            async def process_evs_name_change(message: types.Message, state: FSMContext):
                async with state.proxy() as EVS_ch_n:
                    EVS_ch_n['new_name'] = message.text
                    ch_s_evs = EVS(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                                   user_data['project_ID']).change_name_of_evs(EVS_ch_n['name'],
                                                                               EVS_ch_n['new_name'])
                await state.finish()
                await message.answer('Имя EVS изменено', reply_markup=keyboard_choose)

    @dp.message_handler(lambda message: message.text == 'Редактировать ECS')
    async def modify_ecs(message: types.Message):
        await message.answer('Что редактируем?', reply_markup=keyboard_modify_ecs)

        @dp.message_handler(lambda message: message.text == 'Изменить имя ECS')
        async def modify_ecs_n(message: types.Message):
            await Change_name.name.set()
            await message.answer('Введите старое имя ECS')

            @dp.message_handler(state=Change_name.name)
            async def process_ecs_name_ch(message: types.Message, state: FSMContext):
                async with state.proxy() as ECS_ch_n:
                    ECS_ch_n['name'] = message.text
                await Change_name.name.next()
                await message.answer('Введите новое имя ECS')

            @dp.message_handler(state=Change_name.new_name)
            async def process_evs_name_change(message: types.Message, state: FSMContext):
                async with state.proxy() as ECS_ch_n:
                    ECS_ch_n['new_name'] = message.text
                    ch_s_ecs = ECS(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                                   user_data['project_ID']).change_name_of_ecs(ECS_ch_n['name'],
                                                                               ECS_ch_n['new_name'])
                await state.finish()
                await message.answer('Имя ECS изменено', reply_markup=keyboard_choose)


@dp.message_handler(lambda message: message.text == 'Редактировать VPC')
async def modify_vpc(message: types.Message):
    await message.answer('Что редактируем?', reply_markup=keyboard_modify_vpc)

    @dp.message_handler(lambda message: message.text == 'Изменить имя VPC')
    async def modify_vpc_n(message: types.Message):
        await Change_name.name.set()
        await message.answer('Введите старое имя VPC')

        @dp.message_handler(state=Change_name.name)
        async def process_vpc_name_ch(message: types.Message, state: FSMContext):
            async with state.proxy() as VPC_ch_n:
                VPC_ch_n['name'] = message.text
            await Change_name.name.next()
            await message.answer('Введите новое имя VPC')

        @dp.message_handler(state=Change_name.new_name)
        async def process_vpc_name_change(message: types.Message, state: FSMContext):
            async with state.proxy() as VPC_ch_n:
                VPC_ch_n['new_name'] = message.text
                ch_s_vpc = VPC(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                               user_data['project_ID']).change_name_of_vpc(VPC_ch_n['name'], VPC_ch_n['new_name'])
            await state.finish()
            await message.answer('Имя VPC изменено', reply_markup=keyboard_choose)


@dp.message_handler(lambda message: message.text == 'Редактировать VPC Subnet')
async def modify_vpc_sub(message: types.Message):
    await message.answer('Что редактируем?', reply_markup=keyboard_modify_vpc_sub)

    @dp.message_handler(lambda message: message.text == 'Изменить имя VPC Subnet')
    async def modify_vpc_sub_n(message: types.Message):
        await Change_name.name.set()
        await message.answer('Введите старое имя VPC Subnet')

        @dp.message_handler(state=Change_name.name)
        async def process_vpc_sub_name_ch(message: types.Message, state: FSMContext):
            async with state.proxy() as VPC_s_ch_n:
                VPC_s_ch_n['name'] = message.text
            await Change_name.name.next()
            await message.answer('Введите новое имя VPC Subnet')

        @dp.message_handler(state=Change_name.new_name)
        async def process_vpc_sub_name_change(message: types.Message, state: FSMContext):
            async with state.proxy() as VPC_s_ch_n:
                VPC_s_ch_n['new_name'] = message.text
                ch_s_vpc = VPC(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                               user_data['project_ID']).change_name_of_subnet(VPC_s_ch_n['name'],
                                                                              VPC_s_ch_n['new_name'])
            await state.finish()
            await message.answer('Имя VPC Subnet изменено', reply_markup=keyboard_choose)


@dp.message_handler(lambda message: message.text == 'Редактировать ECS')
async def modify_evs(message: types.Message):
    await message.answer('Что редактируем?', reply_markup=keyboard_modify_ecs)

    @dp.message_handler(lambda message: message.text == 'Изменить имя ECS')
    async def modify_ecs_n(message: types.Message):
        await Change_name.name.set()
        await message.answer('Введите старое имя ECS')

        @dp.message_handler(state=Change_name.name)
        async def process_ecs_name_ch(message: types.Message, state: FSMContext):
            async with state.proxy() as ECS_ch_n:
                ECS_ch_n['name'] = message.text
            await Change_name.name.next()
            await message.answer('Введите новое имя ECS')

        @dp.message_handler(state=Change_name.new_name)
        async def process_ecs_name_change(message: types.Message, state: FSMContext):
            async with state.proxy() as ECS_ch_n:
                ECS_ch_n['new_name'] = message.text
                ch_s_ecs = ECS(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                               user_data['project_ID']).change_name_of_ecs(ECS_ch_n['name'], ECS_ch_n['new_name'])
            await state.finish()
            await message.answer('Имя ECS изменено', reply_markup=keyboard_choose)


@dp.message_handler(lambda message: message.text == 'Редактировать RDS')
async def modify_evs(message: types.Message):
    await message.answer('Что редактируем?', reply_markup=keyboard_modify_rds)

    @dp.message_handler(lambda message: message.text == 'Изменить имя RDS')
    async def modify_rds_n(message: types.Message):
        await Change_name.name.set()
        await message.answer('Введите старое имя RDS')

        @dp.message_handler(state=Change_name.name)
        async def process_rds_name_ch(message: types.Message, state: FSMContext):
            async with state.proxy() as RDS_ch_n:
                RDS_ch_n['name'] = message.text
            await Change_name.name.next()
            await message.answer('Введите новое имя RDS')

        @dp.message_handler(state=Change_name.new_name)
        async def process_rds_name_change(message: types.Message, state: FSMContext):
            async with state.proxy() as RDS_ch_n:
                RDS_ch_n['new_name'] = message.text
                ch_s_rds = RDS(user_data['access_Key_Id'], user_data['secret_Access_Key'],
                               user_data['project_ID']).change_name_of_rds(RDS_ch_n['name'], RDS_ch_n['new_name'])
            await state.finish()
            await message.answer('Имя RDS изменено', reply_markup=keyboard_choose)


if __name__ == '__main__':
    executor.start_polling(dp)