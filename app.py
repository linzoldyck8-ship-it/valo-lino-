<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wiki - Mi Servidor de Minecraft</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                    colors: {
                        wiki: {
                            dark: '#0a0a0a',
                            nav: '#111111',
                            sidebar: '#1a1a1a',
                            bg: '#141b26',
                            card: '#1e293b',
                            cardhover: '#334155',
                            border: '#334155',
                            accent: '#3b82f6',
                            mcgreen: '#22c55e',
                            gold: '#fbbf24'
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            /* Simulating a Minecraft night sky / end dimension background */
            background: radial-gradient(circle at center, #1e293b 0%, #0f172a 50%, #020617 100%);
            background-attachment: fixed;
            color: #e2e8f0;
            overflow-x: hidden;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0f172a; 
        }
        ::-webkit-scrollbar-thumb {
            background: #475569; 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #64748b; 
        }

        .glass-panel {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(71, 85, 105, 0.5);
        }

        .minecraft-text-shadow {
            text-shadow: 2px 2px 0px rgba(0,0,0,0.7);
        }
    </style>
</head>
<body class="antialiased min-h-screen flex flex-col pt-14 pl-0 md:pl-16">

    <!-- Top Navigation Bar -->
    <nav class="fixed top-0 left-0 w-full h-14 bg-wiki-nav border-b border-wiki-border z-50 flex items-center justify-between px-4">
        <div class="flex items-center gap-4">
            <div class="md:hidden text-white cursor-pointer">
                <i class="fa-solid fa-bars text-xl"></i>
            </div>
            <a href="#" class="text-white font-black text-xl tracking-wider flex items-center gap-2">
                <i class="fa-solid fa-cube text-wiki-mcgreen"></i> WIKI<span class="text-gray-400 font-normal">CRAFT</span>
            </a>
        </div>
        
        <div class="hidden md:flex flex-1 max-w-xl mx-4 relative">
            <input type="text" placeholder="Buscar en la wiki..." class="w-full bg-gray-800 text-white border border-gray-700 rounded-full py-1.5 pl-10 pr-4 focus:outline-none focus:border-wiki-accent transition-colors">
            <i class="fa-solid fa-search absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
        </div>

        <div class="flex items-center gap-3">
            <button class="hidden sm:block text-sm font-semibold text-gray-300 hover:text-white">INICIAR SESIÓN</button>
            <button class="bg-wiki-gold text-black font-bold text-xs sm:text-sm px-4 py-1.5 rounded-sm hover:bg-yellow-400 transition-colors uppercase tracking-wide">
                Crear Cuenta
            </button>
        </div>
    </nav>

    <!-- Left Sidebar (Desktop) -->
    <aside class="fixed top-14 left-0 w-16 h-[calc(100vh-3.5rem)] bg-wiki-sidebar border-r border-wiki-border z-40 hidden md:flex flex-col items-center py-4 gap-6 overflow-y-auto">
        <div class="flex flex-col items-center gap-1 text-gray-400 hover:text-wiki-accent cursor-pointer group">
            <i class="fa-solid fa-house text-xl group-hover:scale-110 transition-transform"></i>
            <span class="text-[10px] uppercase">Inicio</span>
        </div>
        <div class="flex flex-col items-center gap-1 text-gray-400 hover:text-wiki-accent cursor-pointer group">
            <i class="fa-solid fa-compass text-xl group-hover:scale-110 transition-transform"></i>
            <span class="text-[10px] uppercase">Explora</span>
        </div>
        <div class="flex flex-col items-center gap-1 text-gray-400 hover:text-wiki-accent cursor-pointer group">
            <i class="fa-solid fa-bookmark text-xl group-hover:scale-110 transition-transform"></i>
            <span class="text-[10px] uppercase">Guardado</span>
        </div>
        <div class="flex flex-col items-center gap-1 text-gray-400 hover:text-wiki-accent cursor-pointer group">
            <i class="fa-solid fa-clock-rotate-left text-xl group-hover:scale-110 transition-transform"></i>
            <span class="text-[10px] uppercase">Historial</span>
        </div>
        <div class="mt-auto flex flex-col items-center gap-1 text-gray-400 hover:text-white cursor-pointer group">
            <i class="fa-solid fa-ellipsis text-xl"></i>
            <span class="text-[10px] uppercase">Más</span>
        </div>
    </aside>

    <!-- Main Content Wrapper -->
    <main class="flex-1 w-full max-w-7xl mx-auto p-4 md:p-6 lg:p-8 relative z-10">
        
        <!-- Main Glass Container (Fandom Wiki Style) -->
        <div class="glass-panel rounded-xl shadow-2xl overflow-hidden mb-8">
            
            <!-- Wiki Header Section -->
            <div class="bg-gradient-to-b from-slate-800 to-slate-900 border-b border-wiki-border p-6 flex flex-col md:flex-row items-center gap-6 relative">
                <!-- Floating background decorative elements -->
                <div class="absolute top-0 right-0 opacity-10 pointer-events-none">
                    <i class="fa-solid fa-dragon text-9xl"></i>
                </div>

                <!-- Server Logo/Icon -->
                <div class="w-24 h-24 md:w-32 md:h-32 bg-gray-900 border-4 border-wiki-border rounded-lg shadow-lg flex items-center justify-center relative overflow-hidden flex-shrink-0">
                    <img src="https://placehold.co/200x200/1e293b/a8a29e?text=Server+Logo" alt="Server Logo" class="w-full h-full object-cover">
                </div>
                
                <!-- Wiki Info & Nav -->
                <div class="flex-1 text-center md:text-left z-10">
                    <p class="text-gray-400 text-sm tracking-widest uppercase mb-1">Bienvenido a</p>
                    <h1 class="text-3xl md:text-5xl font-black text-white mb-2 minecraft-text-shadow">WIKI DEL SERVIDOR</h1>
                    <p class="text-gray-300 text-sm md:text-base max-w-2xl">La fuente principal de información sobre nuestro servidor de Minecraft. Descubre guías de supervivencia, información sobre jefes custom, economía y especializaciones de clases.</p>
                    
                    <!-- Wiki Sub Navigation -->
                    <div class="flex flex-wrap items-center justify-center md:justify-start gap-4 mt-6 text-sm font-semibold">
                        <a href="#" class="text-white border-b-2 border-wiki-accent pb-1 flex items-center gap-2"><i class="fa-solid fa-book-open"></i> EXPLORA</a>
                        <a href="#" class="text-gray-400 hover:text-white transition-colors flex items-center gap-2"><i class="fa-solid fa-khanda"></i> OBJETOS <i class="fa-solid fa-caret-down text-xs"></i></a>
                        <a href="#" class="text-gray-400 hover:text-white transition-colors flex items-center gap-2"><i class="fa-solid fa-skull"></i> JEFES <i class="fa-solid fa-caret-down text-xs"></i></a>
                    </div>
                </div>

                <!-- Top Right Stats -->
                <div class="hidden lg:flex flex-col items-end text-right z-10 border-l border-wiki-border pl-6">
                    <div class="text-3xl font-black text-white">1,420</div>
                    <div class="text-xs text-gray-400 uppercase tracking-wider">Páginas</div>
                    <div class="flex gap-3 mt-2 text-gray-400">
                        <i class="fa-solid fa-comments hover:text-white cursor-pointer"></i>
                        <i class="fa-solid fa-sun hover:text-white cursor-pointer"></i>
                    </div>
                </div>
            </div>

            <!-- Content Grid Area -->
            <div class="p-4 md:p-6 bg-slate-900/50">
                
                <!-- Full Width Banner Alert -->
                <div class="w-full bg-gradient-to-r from-green-900/40 to-blue-900/40 border border-green-700/50 rounded-lg p-4 mb-6 flex items-center gap-4 hover:border-green-500 transition-colors cursor-pointer">
                    <i class="fa-solid fa-map text-2xl text-wiki-mcgreen drop-shadow-lg"></i>
                    <div>
                        <h3 class="text-white font-bold text-lg">Guía del Principiante</h3>
                        <p class="text-gray-300 text-sm">¿Acabas de unirte al servidor? Lee esta guía para sobrevivir tu primera noche y elegir tu clase.</p>
                    </div>
                </div>

                <!-- 3 Column Grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    
                    <!-- Left Column -->
                    <div class="flex flex-col gap-6">
                        <!-- Welcome Card -->
                        <div class="bg-wiki-card border border-wiki-border rounded-lg overflow-hidden group hover:border-gray-500 transition-colors">
                            <div class="bg-slate-800 p-3 border-b border-wiki-border flex items-center gap-2">
                                <i class="fa-solid fa-tree text-wiki-mcgreen"></i>
                                <h2 class="font-bold text-white">¡Bienvenido a la Wiki!</h2>
                            </div>
                            <div class="p-4 text-sm text-gray-300 space-y-3">
                                <p>La enciclopedia en español dedicada a recopilar toda la información sobre nuestro Servidor Custom de Minecraft.</p>
                                <p>Aquí encontrarás detalles sobre mecánicas únicas, economía regulada, facciones y el lore en constante expansión creado por nuestra comunidad.</p>
                            </div>
                        </div>

                        <!-- Statistics Card -->
                        <div class="bg-wiki-card border border-wiki-border rounded-lg overflow-hidden relative">
                            <div class="bg-slate-800 p-3 border-b border-wiki-border flex justify-between items-center">
                                <h2 class="font-bold text-white flex items-center gap-2"><i class="fa-solid fa-chart-line text-blue-400"></i> Estadísticas</h2>
                                <i class="fa-solid fa-server text-gray-400"></i>
                            </div>
                            <div class="p-4 text-sm text-center grid grid-cols-2 gap-4">
                                <div>
                                    <div class="text-gray-400 text-xs uppercase mb-1">Páginas</div>
                                    <div class="text-2xl font-bold text-white">1,420</div>
                                </div>
                                <div>
                                    <div class="text-gray-400 text-xs uppercase mb-1">Ediciones</div>
                                    <div class="text-2xl font-bold text-white">45,892</div>
                                </div>
                                <div>
                                    <div class="text-gray-400 text-xs uppercase mb-1">Archivos</div>
                                    <div class="text-2xl font-bold text-white">3,105</div>
                                </div>
                                <div>
                                    <div class="text-gray-400 text-xs uppercase mb-1">Usuarios</div>
                                    <div class="text-2xl font-bold text-white">842</div>
                                </div>
                            </div>
                            <div class="p-2 bg-slate-800/50 text-center text-xs text-gray-400 border-t border-wiki-border">
                                Actualizado: Hoy
                            </div>
                        </div>
                    </div>

                    <!-- Middle Column -->
                    <div class="flex flex-col gap-6 lg:col-span-2">
                        
                        <!-- Special Feature Banner (e.g. New Update) -->
                        <div class="bg-wiki-card border border-wiki-border rounded-lg overflow-hidden relative group">
                            <div class="h-40 overflow-hidden relative">
                                <img src="https://placehold.co/800x300/1e293b/475569?text=Actualizacion+1.5+End+Update" alt="Update Banner" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                                <div class="absolute inset-0 bg-gradient-to-t from-wiki-card to-transparent"></div>
                                <div class="absolute bottom-4 left-4">
                                    <span class="bg-red-600 text-white text-xs font-bold px-2 py-1 rounded uppercase tracking-wider mb-2 inline-block">Nuevo Parche</span>
                                    <h2 class="text-2xl font-black text-white minecraft-text-shadow">Temporada 4: El Vacío Resurge</h2>
                                </div>
                            </div>
                            <div class="p-4 bg-wiki-card text-sm text-gray-300">
                                <p>La actualización 1.5 ya está disponible en el servidor. Hemos renovado completamente la dimensión del End, añadido 3 nuevos biomas personalizados y el sistema de forja rúnica. <a href="#" class="text-wiki-accent hover:underline">Leer las notas del parche completas...</a></p>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 gap-6">
                            <!-- Updates/Versions Column -->
                            <div class="bg-wiki-card border border-wiki-border rounded-lg overflow-hidden">
                                <div class="bg-slate-800 p-3 border-b border-wiki-border flex justify-between items-center">
                                    <h2 class="font-bold text-white flex items-center gap-2"><i class="fa-solid fa-code-merge text-purple-400"></i> Últimas Versiones</h2>
                                    <div class="flex gap-2 text-gray-400">
                                        <i class="fa-brands fa-java hover:text-white cursor-pointer"></i>
                                        <i class="fa-brands fa-windows hover:text-white cursor-pointer"></i>
                                    </div>
                                </div>
                                <div class="p-0 text-sm text-gray-300">
                                    <ul class="divide-y divide-wiki-border">
                                        <li class="p-3 hover:bg-wiki-cardhover transition-colors cursor-pointer flex justify-between items-center">
                                            <div>
                                                <span class="block font-bold text-white text-base">v1.5.2 (Actual)</span>
                                                <span class="text-xs text-gray-400">Hotfix de Economía</span>
                                            </div>
                                            <span class="text-wiki-accent text-xs">Hoy</span>
                                        </li>
                                        <li class="p-3 hover:bg-wiki-cardhover transition-colors cursor-pointer flex justify-between items-center">
                                            <div>
                                                <span class="block font-bold text-white text-base">v1.5.0</span>
                                                <span class="text-xs text-gray-400">The Void Resurgence</span>
                                            </div>
                                            <span class="text-gray-500 text-xs">Hace 2 sem</span>
                                        </li>
                                        <li class="p-3 hover:bg-wiki-cardhover transition-colors cursor-pointer flex justify-between items-center">
                                            <div>
                                                <span class="block font-bold text-gray-400 text-base">v1.4.9</span>
                                                <span class="text-xs text-gray-500">Mascotas Custom</span>
                                            </div>
                                            <span class="text-gray-500 text-xs">Hace 1 mes</span>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>

                <!-- Bosses Section (Full Width Grid Below) -->
                <div class="mt-6 bg-wiki-card border border-wiki-border rounded-lg overflow-hidden">
                    <div class="bg-slate-800 p-4 border-b border-wiki-border flex justify-between items-center">
                        <h2 class="font-bold text-lg text-white flex items-center gap-2"><i class="fa-solid fa-skull-crossbones text-red-500"></i> Jefes Descubiertos</h2>
                        <a href="#" class="text-xs text-wiki-accent hover:underline uppercase font-bold tracking-wider">Ver Todos</a>
                    </div>
                    <div class="p-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                        
                        <!-- Boss Card 1 -->
                        <div class="group cursor-pointer">
                            <div class="aspect-square bg-slate-900 rounded border border-wiki-border overflow-hidden relative mb-2">
                                <img src="https://placehold.co/200x200/1e1b4b/a5b4fc?text=Rey+Slime" alt="Rey Slime Mutante" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300">
                                <div class="absolute inset-0 border-2 border-transparent group-hover:border-wiki-accent transition-colors rounded"></div>
                            </div>
                            <h3 class="text-center text-sm font-bold text-gray-200 group-hover:text-white">Rey Slime Mutante</h3>
                            <p class="text-center text-xs text-red-400 font-semibold">Nv. 15</p>
                        </div>
                        
                        <!-- Boss Card 2 -->
                        <div class="group cursor-pointer">
                            <div class="aspect-square bg-slate-900 rounded border border-wiki-border overflow-hidden relative mb-2">
                                <img src="https://placehold.co/200x200/3f3f46/f4f4f5?text=Golem+Hierro" alt="Golem Primigenio" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300">
                                <div class="absolute inset-0 border-2 border-transparent group-hover:border-wiki-accent transition-colors rounded"></div>
                            </div>
                            <h3 class="text-center text-sm font-bold text-gray-200 group-hover:text-white">Golem Primigenio</h3>
                            <p class="text-center text-xs text-red-400 font-semibold">Nv. 30</p>
                        </div>

                        <!-- Boss Card 3 -->
                        <div class="group cursor-pointer">
                            <div class="aspect-square bg-slate-900 rounded border border-wiki-border overflow-hidden relative mb-2">
                                <img src="https://placehold.co/200x200/4c1d95/c4b5fd?text=Wither+Rey" alt="Wither Supremo" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300">
                                <div class="absolute inset-0 border-2 border-transparent group-hover:border-wiki-accent transition-colors rounded"></div>
                            </div>
                            <h3 class="text-center text-sm font-bold text-gray-200 group-hover:text-white">Wither Supremo</h3>
                            <p class="text-center text-xs text-red-400 font-semibold">Nv. 50</p>
                        </div>

                        <!-- Boss Card 4 -->
                        <div class="group cursor-pointer">
                            <div class="aspect-square bg-slate-900 rounded border border-wiki-border overflow-hidden relative mb-2">
                                <img src="https://placehold.co/200x200/020617/cbd5e1?text=Dragon+Vacio" alt="Dragón del Vacío" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300">
                                <div class="absolute inset-0 border-2 border-transparent group-hover:border-wiki-accent transition-colors rounded"></div>
                                <div class="absolute top-1 right-1 bg-wiki-gold text-black text-[10px] font-bold px-1.5 rounded">NUEVO</div>
                            </div>
                            <h3 class="text-center text-sm font-bold text-wiki-gold group-hover:text-yellow-300">Dragón del Vacío</h3>
                            <p class="text-center text-xs text-red-500 font-bold">Nv. 100</p>
                        </div>

                        <!-- Boss Card 5 (Hidden on smaller screens to keep row even) -->
                        <div class="group cursor-pointer hidden lg:block">
                            <div class="aspect-square bg-slate-900 rounded border border-dashed border-gray-600 flex flex-col items-center justify-center text-gray-500 hover:text-white hover:border-white transition-colors mb-2">
                                <i class="fa-solid fa-question text-3xl mb-2"></i>
                                <span class="text-xs font-bold uppercase">Desconocido</span>
                            </div>
                            <h3 class="text-center text-sm font-bold text-gray-500">???</h3>
                        </div>

                    </div>
                </div>

            </div>
        </div>

    </main>

    <!-- Scripts -->
    <script>
        // Add subtle parallax effect to the background header elements
        document.addEventListener('mousemove', (e) => {
            const dragon = document.querySelector('.fa-dragon');
            if(dragon) {
                const x = (window.innerWidth - e.pageX * 2) / 90;
                const y = (window.innerHeight - e.pageY * 2) / 90;
                dragon.style.transform = `translate(${x}px, ${y}px) rotate(-15deg)`;
            }
        });
    </script>
</body>
</html>
