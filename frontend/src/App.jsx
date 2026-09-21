import { useEffect, useState } from "react";
import { BarChart3, Bell, Box, ChevronRight, CircleDollarSign, FileText, LayoutDashboard, LogOut, Menu, Moon, Package, Settings, ShoppingCart, Sun, Users, X } from "lucide-react";
import { api } from "./services/api";

const money = (value) => new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value || 0);

function Login({ onLogin }) {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin123");
  const [show, setShow] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setError(""); setLoading(true);
    try {
      const data = await api.login(username, password);
      localStorage.setItem("mercadopro_token", data.access_token);
      onLogin(data.user);
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  }

  return <main className="login-page">
    <section className="login-card">
      <div className="brand-mark">M</div>
      <h1>Mercado<span>Pro</span></h1>
      <p className="muted">Gestão inteligente para o seu mercado</p>
      <form onSubmit={submit}>
        <label>Usuário<input value={username} onChange={e=>setUsername(e.target.value)} autoComplete="username"/></label>
        <label>Senha<div className="password-wrap"><input type={show ? "text":"password"} value={password} onChange={e=>setPassword(e.target.value)} autoComplete="current-password"/><button type="button" onClick={()=>setShow(!show)}>{show ? "Ocultar":"Mostrar"}</button></div></label>
        {error && <div className="error">{error}</div>}
        <button className="primary full" disabled={loading}>{loading ? "Entrando..." : "Entrar no sistema"}</button>
      </form>
      <small className="demo-note">Ambiente de demonstração • admin / admin123</small>
    </section>
  </main>
}

const menu = [
  ["Dashboard", LayoutDashboard],
  ["PDV / Caixa", ShoppingCart],
  ["Produtos", Package],
  ["Estoque", Box],
  ["Clientes", Users],
  ["Financeiro", CircleDollarSign],
  ["Relatórios", BarChart3],
  ["Configurações", Settings],
];

function Dashboard({ user, onLogout }) {
  const [dark, setDark] = useState(localStorage.getItem("mercadopro_theme") === "dark");
  const [open, setOpen] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    localStorage.setItem("mercadopro_theme", dark ? "dark" : "light");
  }, [dark]);

  useEffect(() => { api.dashboard().then(setData).catch(()=>{}); }, []);

  const cards = [
    ["Vendas hoje", money(data?.sales_today), CircleDollarSign, "Sem vendas registradas"],
    ["Vendas no mês", money(data?.sales_month), BarChart3, "Sem dados ainda"],
    ["Ticket médio", money(data?.average_ticket), ShoppingCart, "Aguardando vendas"],
    ["Estoque baixo", data?.low_stock ?? 0, Package, "Tudo sob controle"],
  ];

  return <div className="app-shell">
    <aside className={open ? "sidebar":"sidebar collapsed"}>
      <div className="side-brand"><div className="brand-mark small">M</div>{open && <strong>Mercado<span>Pro</span></strong>}</div>
      <nav>{menu.map(([name, Icon], i)=><button className={i===0?"active":""} key={name}><Icon size={19}/>{open && <span>{name}</span>}{open && i===0 && <ChevronRight size={15} className="nav-arrow"/>}</button>)}</nav>
      <div className="side-bottom">{open && <div className="store-mini"><span className="status-dot"/> Sistema online</div>}<button className="logout" onClick={onLogout}><LogOut size={18}/>{open && "Sair"}</button></div>
    </aside>

    <main className="content">
      <header className="topbar">
        <button className="icon-btn" onClick={()=>setOpen(!open)}><Menu size={21}/></button>
        <div className="breadcrumb">Início <ChevronRight size={15}/> <strong>Dashboard</strong></div>
        <div className="top-actions">
          <button className="icon-btn" onClick={()=>setDark(!dark)} title="Alterar tema">{dark?<Sun size={19}/>:<Moon size={19}/>}</button>
          <button className="icon-btn notification"><Bell size={19}/><i/></button>
          <div className="user-chip"><div className="avatar">{user.name?.charAt(0) || "A"}</div><div><strong>{user.name}</strong><small>{user.role}</small></div></div>
        </div>
      </header>

      <section className="page">
        <div className="welcome"><div><p className="eyebrow">VISÃO GERAL</p><h2>Olá, {user.name.split(" ")[0]} 👋</h2><p>Acompanhe os principais indicadores do seu mercado.</p></div><button className="primary"><ShoppingCart size={17}/> Nova venda</button></div>

        <div className="cards">{cards.map(([title,value,Icon,desc])=><article className="metric" key={title}><div className="metric-top"><div><span>{title}</span><h3>{value}</h3></div><div className="metric-icon"><Icon size={21}/></div></div><small>{desc}</small></article>)}</div>

        <div className="grid-two">
          <article className="panel"><div className="panel-head"><div><h3>Vendas</h3><p>Desempenho dos últimos 7 dias</p></div><select><option>Últimos 7 dias</option><option>Este mês</option></select></div><div className="chart-empty"><BarChart3 size={35}/><strong>Gráfico preparado para os dados reais</strong><span>As vendas aparecerão aqui quando o módulo de PDV estiver conectado.</span></div></article>
          <article className="panel"><div className="panel-head"><div><h3>Atenções</h3><p>Itens que precisam de acompanhamento</p></div><Bell size={18}/></div><div className="attention"><div className="attention-row"><div className="alert-icon red"><Package size={18}/></div><div><strong>Estoque baixo</strong><span>{data?.low_stock ?? 0} produtos abaixo do mínimo</span></div></div><div className="attention-row"><div className="alert-icon yellow"><FileText size={18}/></div><div><strong>Próximos vencimentos</strong><span>{data?.near_expiry ?? 0} produtos próximos do vencimento</span></div></div><div className="attention-row"><div className="alert-icon blue"><CircleDollarSign size={18}/></div><div><strong>Contas a pagar</strong><span>{money(data?.payables)} previstos</span></div></div></div></article>
        </div>

        <div className="panel demo-banner"><div className="demo-icon"><Package size={22}/></div><div><strong>Fase 1 — Ambiente inicial</strong><p>O login, autenticação, usuários, permissões, banco e dashboard estão estruturados. Os indicadores ainda estão em modo demonstração.</p></div></div>
      </section>
    </main>
  </div>
}

export default function App() {
  const [user, setUser] = useState(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    if (localStorage.getItem("mercadopro_token")) api.me().then(setUser).catch(()=>localStorage.removeItem("mercadopro_token")).finally(()=>setChecking(false));
    else setChecking(false);
  }, []);

  if (checking) return <div className="loading-screen">Carregando MercadoPro...</div>;
  if (!user) return <Login onLogin={setUser}/>;
  return <Dashboard user={user} onLogout={()=>{localStorage.removeItem("mercadopro_token");setUser(null)}}/>;
}
