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

export const OperatorWorkGuide: React.FC = () => (
  <div>
    <Typography.Paragraph style={{ marginBottom: 8 }}>
      Смена в шести шагах: открыть турнир → взять свой день → скопировать ссылку и ключ в OBS → начать эфир →
      отмечать упоминания → остановить эфир.
    </Typography.Paragraph>
    <ol style={listStyle}>
      <li>
        В шапке откройте <Kbd>Оператор</Kbd> или с дашборда нажмите <Kbd>Мероприятия оператора</Kbd>. В списке —
        турниры на сегодня и ближайшую неделю. Карточка, где свободных дней нет, приглушена.
      </li>
      <li>
        Нажмите карточку — откроется пульт. Вверху название турнира и сколько в нём дней.
      </li>
      <li>
        Если день ещё ничей, нажмите <Kbd>Взять в работу</Kbd>, отметьте свои дни и подтвердите. День закрепится за
        вами. <Kbd>Снять с работы</Kbd> — когда смену нужно отдать.
      </li>
      <li>
        <strong>Чек-лист перед эфиром</strong> — шесть пунктов на выбранный день. У каждого дня свой набор галочек.
      </li>
      <li>
        В блоке <strong>Управление эфиром</strong> выберите <Kbd>День</Kbd>. Нажмите <Kbd>Показать</Kbd> у «Параметры
        дня»: ссылка на трансляцию, URL сервера и ключ. У каждого поля есть копирование — вставьте значения в OBS
        или другой энкодер.
      </li>
      <li>
        <Kbd>Начать эфир</Kbd> фиксирует время старта и запускает таймер. Пока эфир не начат, кнопка{' '}
        <Kbd>Добавить упоминание</Kbd> не нажимается.
      </li>
      <li>
        Когда в эфире прозвучало спонсорское упоминание, нажмите <Kbd>Добавить упоминание</Kbd>. Ориентир — четыре
        слота: «Начало эфира», две середины, «Конец эфира». Под кнопками видно, какие слоты уже отмечены.
      </li>
      <li>
        Справа в списке <strong>Упоминания</strong> — таймкод и время по Москве. <Kbd>Корректировка</Kbd> сдвигает
        отметку от старта эфира (минуты и секунды 0–59), затем <Kbd>Сохранить</Kbd>.
      </li>
      <li>
        В конце дня нажмите <Kbd>Остановить эфир</Kbd> и подтвердите. После остановки новые упоминания этого дня
        нельзя добавить, пока эфир не начнут снова.
      </li>
    </ol>
    <Typography.Paragraph type="secondary" style={{ marginTop: 14, marginBottom: 0, fontSize: 13 }}>
      Если день уже у другого оператора, пульт для этого дня закрыт — статус написан над кнопками. Дни между собой
      распределяете вы: менеджер только заводит турнир, ссылки и ключи.
    </Typography.Paragraph>
  </div>
)

export const ManagerWorkGuide: React.FC = () => (
  <div>
    <Typography.Paragraph style={{ marginBottom: 8 }}>
      Менеджер готовит турнир. Эфир и отметки упоминаний делает оператор в своём пульте.
    </Typography.Paragraph>
    <ol style={listStyle}>
      <li>
        В шапке откройте <Kbd>Менеджер</Kbd> или с дашборда нажмите <Kbd>Перейти к трансляциям</Kbd>.
      </li>
      <li>
        <Kbd>Новое мероприятие</Kbd>: название, дата старта и длительность в днях (1–5), затем <Kbd>Создать</Kbd>.
        Можно выбрать шаблон — тогда URL сервера подставится во все дни.
      </li>
      <li>
        Откройте строку турнира. Для каждого <strong>Дня 1…N</strong> заполните ссылку на трансляцию, URL сервера и
        ключ — оператор увидит их в пульте и сможет скопировать. Нажмите <Kbd>Сохранить</Kbd>.
      </li>
      <li>
        Блок <strong>Упоминания оператора</strong> — те же отметки, что оператор ставит во время эфира. Смотреть
        прогресс можно, не заходя в пульт.
      </li>
      <li>
        <strong>Шаблоны мероприятий</strong> запоминают типовую структуру. Кнопка <Kbd>Создать мероприятие</Kbd> в
        карточке шаблона разворачивает новый турнир.
      </li>
      <li>
        <Kbd>Экспорт отчёта</Kbd> выгружает упоминания в Word, CSV или Excel — за период или по одному турниру.
      </li>
    </ol>
    <Typography.Paragraph type="secondary" style={{ marginTop: 14, marginBottom: 0, fontSize: 13 }}>
      День за собой берёт оператор кнопкой «Взять в работу». Назначать операторов на дни в этой панели не нужно.
    </Typography.Paragraph>
  </div>
)

const AdminWorkGuide: React.FC = () => (
  <div>
    <Typography.Paragraph style={{ marginBottom: 8 }}>
      Суперадмин видит разделы менеджера и оператора и заводит учётные записи.
    </Typography.Paragraph>
    <ol style={listStyle}>
      <li>
        <Kbd>Админ</Kbd> — пользователи, журнал действий и аналитика. Новый человек: email, фамилия, имя, роль.
        Пароль уходит ему на почту. В шапке у него появится пункт <Kbd>Как работать</Kbd> с инструкцией его роли.
      </li>
      <li>
        В пульте оператора суперадмин может работать с любым днём и не обязан нажимать «Взять в работу».
      </li>
    </ol>
    <ul style={subListStyle}>
      <li>Роль в форме создания: оператор ведёт эфир, менеджер заводит турниры, суперадмин — полный доступ.</li>
    </ul>
  </div>
)

/** Пошаговая инструкция текущей роли. */
export const PrimaryRoleTraining: React.FC<{ role: UserRole }> = ({ role }) => {
  if (role === 'OPERATOR') {
    return <OperatorWorkGuide />
  }
  if (role === 'STREAM_MANAGER') {
    return <ManagerWorkGuide />
  }
  return (
    <div>
      <AdminWorkGuide />
      <Typography.Title level={5} style={{ marginTop: 20 }}>
        Турниры — как у менеджера
      </Typography.Title>
      <ManagerWorkGuide />
      <Typography.Title level={5} style={{ marginTop: 20 }}>
        Эфир — как у оператора
      </Typography.Title>
      <OperatorWorkGuide />
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
        'Берёт свободный день, копирует ссылку и ключ, начинает эфир, ставит упоминания и останавливает эфир.',
    })
  }
  if (currentRole !== 'STREAM_MANAGER') {
    items.push({
      key: 'mgr',
      title: 'Менеджер',
      body:
        'Создаёт турнир, заполняет ссылки и ключи по дням, смотрит упоминания и выгружает отчёт.',
    })
  }
  if (currentRole !== 'SUPERADMIN') {
    items.push({
      key: 'adm',
      title: 'Суперадминистратор',
      body: 'Заводит пользователей и видит все разделы. Дни операторам не назначает — оператор берёт день сам.',
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
