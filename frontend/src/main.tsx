import { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { Bell, BookOpen, CalendarDays, CheckSquare, ChevronRight, Clock3, GraduationCap, Inbox, LayoutDashboard, Menu, Moon, Settings, Sun, UserRound, X } from 'lucide-react'
import './styles.css'

type Availability = { available: boolean; reason?: string }
type Dashboard = Record<string, Availability>
const api = 'http://localhost:8000/api'

const navigation = [
  ['Accueil', LayoutDashboard], ['Emploi du temps', CalendarDays], ['Notes', GraduationCap], ['Devoirs', CheckSquare], ['Cahier de textes', BookOpen], ['Absences', Clock3], ['Messagerie', Inbox], ['Paramètres', Settings],
] as const

function Unavailable({ item }: { item?: Availability }) {
  return <div className="unavailable"><span className="quiet-dot"/> {item?.reason ?? 'Cette donnée est indisponible pour le moment.'}</div>
}

function App() {
  const [active, setActive] = useState('Accueil')
  const [dark, setDark] = useState(false)
  const [open, setOpen] = useState(false)
  const [data, setData] = useState<Dashboard | null>(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => { document.documentElement.dataset.theme = dark ? 'dark' : 'light' }, [dark])
  useEffect(() => { fetch(`${api}/dashboard`).then(r => r.ok ? r.json() : Promise.reject()).then(setData).catch(() => setData(null)).finally(() => setLoading(false)) }, [])
  const day = new Intl.DateTimeFormat('fr-FR', { weekday:'long', day:'numeric', month:'long' }).format(new Date())
  const item = (key: string) => data?.[key]
  const isHome = active === 'Accueil'
  return <div className="app-shell">
    <aside className={open ? 'sidebar open' : 'sidebar'}>
      <div className="brand"><div className="brand-mark">H</div><span>horizon</span><button className="mobile-close" onClick={() => setOpen(false)} aria-label="Fermer"><X size={19}/></button></div>
      <nav>{navigation.map(([label, Icon]) => <button key={label} className={active === label ? 'nav-item selected' : 'nav-item'} onClick={() => {setActive(label); setOpen(false)}}><Icon size={18}/><span>{label}</span>{label === 'Messagerie' && <i/>}</button>)}</nav>
      <div className="account"><div className="avatar">A</div><div><strong>Mon espace</strong><small>Élève</small></div><ChevronRight size={16}/></div>
    </aside>
    <main>
      <header><button className="menu" onClick={() => setOpen(true)} aria-label="Ouvrir la navigation"><Menu/></button><div className="crumb">Espace élève <span>/</span> {active}</div><div className="top-actions"><button className="icon-button" onClick={() => setDark(!dark)} aria-label="Changer le thème">{dark ? <Sun size={18}/> : <Moon size={18}/>}</button><button className="icon-button" aria-label="Notifications"><Bell size={18}/><b/></button><button className="profile"><UserRound size={18}/></button></div></header>
      {isHome ? <section className="content">
        <div className="hero"><div><p className="eyebrow">{day}</p><h1>Bonjour<em>.</em></h1><p className="subtitle">Voici l’essentiel de votre journée.</p></div><button className="refresh" onClick={() => {setLoading(true); fetch(`${api}/dashboard`).then(r=>r.json()).then(setData).finally(()=>setLoading(false))}}>Actualiser</button></div>
        {loading ? <div className="skeleton-row"><div/><div/><div/></div> : null}
        {!loading && !data ? <div className="notice error">L’API Horizon est indisponible. Vérifiez que le serveur est démarré.</div> : null}
        <div className="grid primary-grid">
          <article className="card next-class"><div className="card-title"><span>Prochain cours</span><Clock3 size={17}/></div><div className="class-empty"><div className="empty-icon"><CalendarDays size={22}/></div><strong>Votre journée vous attend</strong><Unavailable item={item('next_class')}/></div></article>
          <article className="card timetable"><div className="card-title"><span>Emploi du temps</span><button onClick={() => setActive('Emploi du temps')}>Voir tout <ChevronRight size={15}/></button></div><div className="time-empty"><span>09:00</span><div/><p>Aucun cours accessible</p></div><Unavailable item={item('timetable')}/></article>
        </div>
        <div className="section-heading"><div><h2>À suivre</h2><p>Les informations importantes, réunies ici.</p></div></div>
        <div className="grid follow-grid">
          <article className="card mini"><div className="icon-tint lavender"><CheckSquare size={18}/></div><h3>Devoirs</h3><Unavailable item={item('homework')}/><button onClick={()=>setActive('Devoirs')}>Ouvrir les devoirs <ChevronRight size={15}/></button></article>
          <article className="card mini"><div className="icon-tint amber"><GraduationCap size={18}/></div><h3>Résultats</h3><Unavailable item={item('grades')}/><button onClick={()=>setActive('Notes')}>Voir les notes <ChevronRight size={15}/></button></article>
          <article className="card mini"><div className="icon-tint rose"><Clock3 size={18}/></div><h3>Vie scolaire</h3><Unavailable item={item('absences')}/><button onClick={()=>setActive('Absences')}>Consulter <ChevronRight size={15}/></button></article>
        </div>
        <article className="card news"><div className="card-title"><span>Informations de l’établissement</span><Inbox size={17}/></div><Unavailable item={item('news')}/></article>
      </section> : <section className="content page"><p className="eyebrow">Horizon</p><h1>{active}</h1><p className="subtitle">Cette section affichera les données fournies par votre établissement dès que votre connexion Pronote sera configurée.</p><article className="card empty-page"><div className="empty-icon"><BookOpen size={24}/></div><h2>Aucune donnée à afficher</h2><p>Horizon ne crée pas de données scolaires de démonstration. Vérifiez votre connexion dans les paramètres.</p><button className="primary" onClick={()=>setActive('Paramètres')}>Ouvrir les paramètres</button></article></section>}
    </main>
  </div>
}
createRoot(document.getElementById('root')!).render(<App />)
