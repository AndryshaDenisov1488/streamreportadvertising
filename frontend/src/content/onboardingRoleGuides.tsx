import { Typography } from 'antd'
import React from 'react'

import type { UserRole } from '@/api/types'

const listStyle: React.CSSProperties = {
  margin: '10px 0 0',
  paddingLeft: 22,
  color: '#334155',
  lineHeight: 1.7,
}

const subListStyle: React.CSSProperties = {
  margin: '6px 0 0',
  paddingLeft: 18,
  color: '#64748b',
  lineHeight: 1.6,
  fontSize: 13,
}

const Kbd: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <Typography.Text strong style={{ color: '#0284c7' }}>{children}</Typography.Text>
)

/** Детальное обучение под роль текущего пользователя (без тавтологии с «другими ролями»). */
export const PrimaryRoleTraining: React.FC<{ role: UserRole }> = ({ role }) => {
  if (role === 'OPERATOR') {
    return (
      <div>
        <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
          Ниже — порядок действий в интерфейсе: те же подписи кнопок, что в панели.
        </Typography.Paragraph>
        <ol style={listStyle}>
          <li>
            В шапке откройте раздел <Kbd>Оператор</Kbd> (маршрут <Typography.Text code>/operator</Typography.Text>) —
            список мероприятий, где вас назначили. Нажмите на строку турнира.
          </li>
          <li>
            Откроется <strong>Пульт оператора</strong>. Вверху — название мероприятия и длительность в днях.
          </li>
          <li>
            <strong>Статус и дни:</strong> если день свободен, нажмите <Kbd>Взять в работу</Kbd>, в модальном окне
            отметьте нужные дни и подтвердите. Тогда этот день закрепляется за вами. Кнопка{' '}
            <Kbd>Снять с работы</Kbd> снимает ваши назначения (когда нужно передать смену).
          </li>
          <li>
            Блок <strong>Чек-лист перед эфиром</strong> (для выбранного дня) — шесть пунктов перед стартом; у каждого дня свой
            набор галочек.
          </li>
          <li>
            В <strong>Управление эфиром</strong> выберите <Kbd>День</Kbd> в выпадающем списке. Раскройте{' '}
            <Kbd>Показать</Kbd> у «Параметры дня» — там ссылка на трансляцию, URL сервера и ключ. У каждого поля есть
            копирование (иконка «копировать» / подсказка «Скопировано») — вставьте в OBS или другой энкодер.
          </li>
          <li>
            Нажмите <Kbd>Начать эфир</Kbd> — фиксируется время старта, запускается <strong>таймер эфира</strong>. Без
            активного эфира кнопка <Kbd>Добавить упоминание</Kbd> недоступна.
          </li>
          <li>
            Во время эфира нажимайте <Kbd>Добавить упоминание</Kbd>, когда в эфире произошло спонсорское упоминание.
            Ориентируйтесь на план из четырёх слотов: «Начало эфира», две середины, «Конец эфира» — блок под кнопками
            показывает, какие шаги уже отмечены.
          </li>
          <li>
            Справа в списке <strong>Упоминания</strong> видны таймкоды и время (МСК). У записи нажмите{' '}
            <Kbd>Корректировка</Kbd> — в модалке задайте смещение от старта эфира (минуты и секунды 0–59) и{' '}
            <Kbd>Сохранить</Kbd>, если нужно поправить таймкод после эфира.
          </li>
          <li>
            По окончании дня нажмите <Kbd>Остановить эфир</Kbd> и подтвердите в диалоге. После остановки новые упоминания
            для этого дня до следующего старта создать нельзя.
          </li>
        </ol>
        <Typography.Paragraph type="secondary" style={{ marginTop: 14, marginBottom: 0, fontSize: 13 }}>
          Если день назначен другому оператору, пульт для него заблокирован — это видно по статусу над кнопками.
        </Typography.Paragraph>
      </div>
    )
  }

  if (role === 'STREAM_MANAGER') {
    return (
      <div>
        <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
          Как завести эфир и подготовить дни для операторов.
        </Typography.Paragraph>
        <ol style={listStyle}>
          <li>
            В шапке откройте раздел трансляций — <Kbd>Перейти к трансляциям</Kbd> (
            <Typography.Text code>/manager</Typography.Text>).
          </li>
          <li>
            Нажмите <Kbd>Новое мероприятие</Kbd>: укажите <strong>название</strong>, <strong>дату старта</strong> и{' '}
            <strong>длительность в днях</strong> (1–5), затем <Kbd>Создать</Kbd>.
          </li>
          <li>
            В таблице «Мероприятия» нажмите на строку или ссылку открытия — попадёте в <strong>карточку мероприятия</strong>{' '}
            (редактирование).
          </li>
          <li>
            В карточке заполните <strong>Название</strong>, <strong>дату старта</strong> и <strong>число дней</strong>.
            Ниже для каждого <strong>Дня 1…N</strong> введите: ссылку на трансляцию, URL сервера и ключ — их операторы
            увидят в пульте (с копированием). Нажмите <Kbd>Сохранить</Kbd>.
          </li>
          <li>
            Блок <strong>Упоминания оператора</strong> — тот же список отметок, что видит оператор во время эфира
            (удобно контролировать без входа в пульт).
          </li>
          <li>
            На странице менеджера доступны <strong>Шаблоны мероприятий</strong>: можно сохранить типовую структуру и кнопкой{' '}
            <Kbd>Создать мероприятие</Kbd> развернуть новый турнир из шаблона.
          </li>
          <li>
            Кнопка <Kbd>Экспорт отчёта</Kbd> открывает выгрузку упоминаний (Word, CSV, Excel) за период или по мероприятию —
            для отчётности спонсорам.
          </li>
        </ol>
        <Typography.Paragraph type="secondary" style={{ marginTop: 14, marginBottom: 0, fontSize: 13 }}>
          Назначение операторов на конкретные дни делается в рабочем процессе федерации; в пульте оператор затем жмёт{' '}
          <Kbd>Взять в работу</Kbd> по свободным дням.
        </Typography.Paragraph>
      </div>
    )
  }

  return (
    <div>
      <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
        У вас доступ ко всем разделам панели: как у менеджера и оператора, плюс администрирование.
      </Typography.Paragraph>
      <ol style={listStyle}>
        <li>
          <Kbd>Перейти к трансляциям</Kbd> — создание мероприятий, дни, URL/ключи, шаблоны, экспорт отчётов (см. инструкцию для
          менеджера выше по смыслу).
        </li>
        <li>
          <Kbd>Оператор</Kbd> — пульт эфира: эфир, упоминания, корректировка таймкодов (см. инструкцию для оператора).
        </li>
        <li>
          В пульте оператора суперадмин может работать с любыми днями без ограничения «взять день».
        </li>
        <li>
          Раздел <Kbd>Администрирование</Kbd> (<Typography.Text code>/admin</Typography.Text>) — пользователи, аудит,
          продуктовая аналитика.
        </li>
      </ol>
      <ul style={subListStyle}>
        <li>Создание учётных записей и приветственные письма с временным паролем.</li>
        <li>Журнал действий и сводки по действиям в интерфейсе (аналитика).</li>
      </ul>
    </div>
  )
}

/** Кратко о других ролях — одна строка, без повторения текста «вашей» роли. */
export const OtherRolesHint: React.FC<{ currentRole: UserRole }> = ({ currentRole }) => {
  const items: { key: string; title: string; body: string }[] = []
  if (currentRole !== 'OPERATOR') {
    items.push({
      key: 'op',
      title: 'Оператор',
      body:
        'Пульт эфира: взять день, чек-лист, копирование ссылок/ключа, Начать/Остановить эфир, Добавить упоминание, Корректировка таймкода.',
    })
  }
  if (currentRole !== 'STREAM_MANAGER') {
    items.push({
      key: 'mgr',
      title: 'Менеджер',
      body:
        'Создание мероприятий и дней, заполнение URL/ключей, шаблоны, экспорт отчётов, просмотр упоминаний в карточке мероприятия.',
    })
  }
  if (currentRole !== 'SUPERADMIN') {
    items.push({
      key: 'adm',
      title: 'Суперадминистратор',
      body: 'Пользователи, аудит, аналитика, полный доступ к мероприятиям и пульту.',
    })
  }
  if (items.length === 0) {
    return null
  }
  return (
    <>
      {items.map((it) => (
        <Typography.Paragraph key={it.key} type="secondary" style={{ marginBottom: 10 }}>
          <Typography.Text strong style={{ color: '#0f172a' }}>{it.title}:</Typography.Text> {it.body}
        </Typography.Paragraph>
      ))}
    </>
  )
}
