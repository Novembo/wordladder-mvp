/**
 * Local Client-Side Word Ladder Game Engine.
 * Allows 100% standalone, offline, zero-backend play directly in the browser
 * (ideal for GitHub Pages and when Render free-tier is sleeping/offline).
 */

const TIME_LIMITS = { basic: 80, intermediate: 60, advanced: 40 }
const MIN_START_NEIGHBORS = 3
const MAX_LIVES = 3

export const SYNONYMS_DB = {
  fr: {
    chat: 'Félin domestique qui miaule (ou matou)',
    char: "Véhicule tiré par des chevaux ou char d'assaut",
    cher: 'Qui coûte beaucoup d’argent (ou personne aimée)',
    chez: 'Au domicile de quelqu’un',
    chef: 'Personne qui dirige une équipe ou cuisinier',
    clef: 'Outil pour ouvrir une serrure',
    bleu: 'Couleur du ciel par temps clair',
    bloc: 'Grosse masse solide de pierre ou de bois',
    bras: 'Membre supérieur reliant l’épaule à la main',
    gris: 'Mélange de noir et de blanc',
    gros: 'De taille ou de volume supérieur à la moyenne',
    gras: 'Riche en matière grasse ou graisseux',
    gens: 'Personnes en général',
    dent: 'Organe blanc dans la bouche pour mâcher',
    vent: 'Mouvement de l’air dans l’atmosphère',
    vert: 'Couleur de l’herbe et des feuilles',
    vers: 'Ligne de poésie ou en direction de',
    pere: 'Papa de la famille',
    mere: 'Maman de la famille',
    mare: 'Petite étendue d’eau calme pour les canards',
    gare: 'Station où s’arrêtent les trains',
    page: 'Côté d’une feuille de livre ou jeune valet',
    sage: 'Prudent, calme et raisonnable',
    cage: 'Enclos à barreaux pour animaux ou oiseaux',
    nage: 'Déplacement dans l’eau',
    pain: 'Aliment cuit à base de farine et d’eau',
    bain: 'Immersion dans l’eau pour se laver ou se détendre',
    main: 'Partie du corps humain avec cinq doigts',
    jour: 'Période éclairée entre le lever et le coucher du soleil',
    four: 'Appareil pour cuire le pain ou les gâteaux',
    tour: 'Construction élevée ou promenade circulaire',
    cour: 'Espace découvert entouré de bâtiments',
    peur: 'Sentiment d’inquiétude ou d’angoisse',
    loup: 'Grand carnivore sauvage de la forêt',
    coup: 'Choc brutal ou impact',
    lire: 'Déchiffrer des mots écrits dans un livre',
    rire: 'Manifester sa joie par des éclats sonores',
    dire: 'Exprimer par la parole',
    port: 'Abri pour les bateaux au bord de la mer',
    fort: 'Qui a beaucoup de puissance ou château fort',
    pont: 'Construction permettant de traverser un fleuve',
    rame: 'Aviron pour faire avancer une barque',
    dame: 'Femme adulte respectée',
    plante: 'Végétal avec des feuilles et des racines',
    plat: 'Sans relief ou assiette de cuisine',
    plan: 'Schéma, dessin ou stratégie',
    porte: 'Ouverture pour entrer dans une pièce',
    piste: 'Chemin tracé pour courir ou skier',
    liste: 'Suite de mots ou d’objets notés par écrit',
    balle: 'Objet sphérique pour jouer au tennis ou foot',
    ville: 'Grande agglomération avec des rues et maisons',
  },
  en: {
    cold: 'Opposite of hot; chilly or freezing',
    cord: 'Thick string, rope, or electric cable',
    card: 'Rectangular piece of paper, game card',
    ward: 'A room in a hospital or to fend off',
    warm: 'Pleasantly heated, not hot and not cold',
    worm: 'Small, long creature that lives in soil',
    word: 'A single distinct meaningful element of speech',
    wood: 'Hard material that trees are made of',
    wool: 'Warm soft fabric made from sheep hair',
    fool: 'A silly person or a court jester',
    food: 'What people and animals eat to live',
    foot: 'The bottom part of your leg used for walking',
    fort: 'A fortified military building or stronghold',
    form: 'Shape, document to fill in, or configuration',
    farm: 'Area of land used for growing crops and animals',
    firm: 'Solid and steady, or a company business',
    fire: 'Flames producing heat, light, and smoke',
    live: 'To be alive or reside in a house',
    line: 'A long narrow mark or row of people',
    bone: 'Hard white part inside vertebrate bodies',
    bank: 'Place where money is kept, or river edge',
    bark: 'Outer skin of a tree, or the sound a dog makes',
    dark: 'Absence of light; nighttime',
    dart: 'Small pointed missile thrown at a target',
    part: 'A piece or section of a whole',
    past: 'Time that has already happened; history',
    post: 'Mail letter, upright pole, or social media message',
    host: 'Person who entertains guests',
    most: 'Greatest in amount or number',
    cost: 'Price of an object or money required',
    cast: 'Throw something or actors in a play',
    case: 'Instance, container, or suitcase',
    cave: 'Natural underground hollow chamber',
    gate: 'Movable barrier in a fence or wall',
    hate: 'Intense feeling of dislike or hostility',
    date: 'Day of the month, or sweet brown palm fruit',
    head: 'Top part of the body with brain and face',
    lead: 'To guide others or heavy metal',
    boat: 'Small water vessel traveling on lakes/rivers',
    coat: 'Warm garment worn outdoors over clothes',
    chat: 'Friendly informal conversation',
    that: 'Referring to a specific thing previously mentioned',
    what: 'Question word used to ask about things',
    wait: 'Stay in place until an event happens',
    ball: 'Round toy used in football, tennis, and games',
    fall: 'Drop downward, or autumn season',
    tall: 'Of great height; opposite of short',
    bell: 'Hollow metal instrument that rings',
    best: 'Highest quality, better than all others',
    rest: 'Relaxation or sleep to regain energy',
    rust: 'Reddish coating formed on iron by oxidation',
    dust: 'Fine dry powder on surfaces',
    star: 'Luminous celestial body in the night sky',
    stay: 'Remain in the same place without leaving',
    stop: 'Cease movement or action immediately',
    game: 'Playful activity or competitive match',
    came: 'Past tense of come',
    name: 'Word by which a person or thing is known',
    time: 'Continuous progress of existence and events',
  },
  es: {
    casa: 'Edificio para habitar; hogar o vivienda',
    cama: 'Mueble blando para dormir y descansar',
    cara: 'Parte anterior de la cabeza humana; rostro',
    cero: 'Número que representa la ausencia de cantidad',
    pero: 'Conjunción adversativa que indica oposición',
    pera: 'Fruta dulce de forma alargada y jugosa',
    pata: 'Pie y pierna de los animales',
    pala: 'Herramienta plana para excavar tierra',
    hola: 'Saludo amistoso y cordial',
    hora: 'Medida de tiempo de sesenta minutos',
    hoja: 'Parte verde y plana de las plantas',
    roja: 'Color encarnado vivo como la sangre',
    ropa: 'Prendas que usamos para vestirnos',
    copa: 'Vaso con pie para beber vino',
    sopa: 'Plato caliente con caldo y fideos o verduras',
    gato: 'Animal felino doméstico que maúlla',
    pato: 'Ave acuática con pico aplanado y patas palmeadas',
    paso: 'Movimiento que se hace al caminar',
    vaso: 'Recipiente para beber líquidos',
    voto: 'Expresión de opinión o elección en urnas',
    moto: 'Vehículo de dos ruedas con motor',
    mono: 'Primate inteligente o prenda de vestir entera',
    mano: 'Parte del cuerpo que tiene cinco dedos',
    vino: 'Bebida alcohólica que se obtiene de la uva',
    pino: 'Árbol de madera blanca y hojas aciculares',
    fino: 'Delgado, suave o de gran calidad',
    hielo: 'Agua congelada convertida en sólido por el frío',
    cielo: 'Bóveda azul donde se ven las nubes y estrellas',
    libro: 'Conjunto de páginas escritas encuadernadas',
    libre: 'Que tiene libertad y no está preso',
    nieve: 'Agua helada que cae de las nubes en copos',
    nuevo: 'Recién hecho o estrenado por primera vez',
    huevo: 'Cuerpo redondeado que ponen las aves',
    fuego: 'Calor y luz producidos por la combustión',
    juego: 'Actividad divertida para entretenerse y aprender',
    vida: 'Existencia de los seres vivos',
  },
}

const packsCache = new Map()

export function clearPacksCache() {
  packsCache.clear()
}

export function stripAccents(str) {
  if (!str) return ''
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim()
}

export function differsByOneLetter(a, b) {
  if (!a || !b || a.length !== b.length) return false
  let diff = 0
  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) {
      diff++
      if (diff > 1) return false
    }
  }
  return diff === 1
}

export async function loadPack(lang = 'fr') {
  if (packsCache.has(lang)) {
    return packsCache.get(lang)
  }

  const base = import.meta.env?.BASE_URL || '/'
  const cleanBase = base.endsWith('/') ? base : base + '/'
  const packUrl = `${cleanBase}packs/${lang}.json`

  try {
    const res = await fetch(packUrl)
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`)
    }
    const pack = await res.json()
    packsCache.set(lang, pack)
    return pack
  } catch (err) {
    // Si échec de chargement relatif, tentative depuis la racine
    if (cleanBase !== '/') {
      const fallbackUrl = `/packs/${lang}.json`
      const res = await fetch(fallbackUrl)
      if (res.ok) {
        const pack = await res.json()
        packsCache.set(lang, pack)
        return pack
      }
    }
    throw new Error(`Impossible de charger le dictionnaire (${lang}): ${err.message}`)
  }
}

export class LocalGameError extends Error {
  constructor(code, message) {
    super(message)
    this.code = code
    this.detail = { code, message }
  }
}

export class LocalMatch {
  constructor(pack, { lang = 'fr', level = 'basic', mode = 'solo', playAllParts = false } = {}) {
    if (!TIME_LIMITS[level]) {
      throw new LocalGameError('bad_level', `Niveau inconnu : ${level}`)
    }
    if (mode !== 'solo' && mode !== 'duo') {
      throw new LocalGameError('bad_mode', `Mode inconnu : ${mode}`)
    }

    this.id = 'loc-' + Math.random().toString(36).substring(2, 10) + '-' + Date.now().toString(36)
    this.pack = pack
    this.lang = lang
    this.level = level
    this.mode = mode
    this.playAllParts = playAllParts

    this.scores = [0, 0]
    this.lives = [MAX_LIVES, MAX_LIVES]
    this.part = 1
    this.timeAdjustment = 0
    this.used = new Set()
    this.current = ''
    this.wordLength = 0
    this.toMove = 0
    this.finished = false
    this.winner = null
    this.lastEvent = ''
    this.turnStarted = Date.now()
    this.deadlineIso = null

    this.startPart()
  }

  get timeLimit() {
    return TIME_LIMITS[this.level] + this.timeAdjustment
  }

  availableFrom(word) {
    const neighbors = this.pack.graph[word] || []
    return neighbors.filter((w) => !this.used.has(w))
  }

  startPart() {
    const levelPool = this.pack.levels?.[this.level] || Object.keys(this.pack.graph)

    if (this.wordLength === 0) {
      let pool = levelPool.filter(
        (w) => !this.used.has(w) && this.availableFrom(w).length >= MIN_START_NEIGHBORS
      )
      if (pool.length === 0) {
        pool = Object.keys(this.pack.graph).filter(
          (w) => !this.used.has(w) && this.availableFrom(w).length > 0
        )
      }
      if (pool.length === 0) {
        throw new LocalGameError('no_start_word', 'Aucun mot de départ disponible.')
      }

      const chosen = pool[Math.floor(Math.random() * pool.length)]
      this.wordLength = chosen.length
      this.current = chosen
    } else {
      let pool = levelPool.filter(
        (w) =>
          w.length === this.wordLength &&
          !this.used.has(w) &&
          this.availableFrom(w).length >= MIN_START_NEIGHBORS
      )
      if (pool.length === 0) {
        pool = Object.keys(this.pack.graph).filter(
          (w) =>
            w.length === this.wordLength &&
            !this.used.has(w) &&
            this.availableFrom(w).length > 0
        )
      }
      if (pool.length === 0) {
        throw new LocalGameError(
          'no_start_word',
          `Aucun mot de départ de ${this.wordLength} lettres disponible.`
        )
      }

      const chosen = pool[Math.floor(Math.random() * pool.length)]
      this.current = chosen
    }

    this.used.add(this.current)
    this.toMove = (this.part - 1) % 2
    this.turnStarted = Date.now()
    this.deadlineIso = new Date(Date.now() + this.timeLimit * 1000).toISOString()

    this.runComputer()
  }

  play(player, word) {
    this.checkTurn(player)

    const w = stripAccents(word)
    if (w.length !== this.wordLength) {
      throw new LocalGameError(
        'wrong_length',
        `Le mot doit comporter exactement ${this.wordLength} lettres.`
      )
    }
    if (!this.pack.graph[w]) {
      throw new LocalGameError('unknown_word', `« ${w} » n'est pas dans le dictionnaire.`)
    }
    if (this.used.has(w)) {
      throw new LocalGameError('already_used', `« ${w} » a déjà été utilisé.`)
    }
    if (!differsByOneLetter(this.current, w)) {
      throw new LocalGameError('not_one_letter', 'Il faut changer exactement une lettre.')
    }

    this.accept(w)
    return this.getState()
  }

  timeout(player) {
    this.checkTurn(player)

    if (this.lives[player] > 1) {
      this.lives[player] -= 1
      this.turnStarted = Date.now()
      this.deadlineIso = new Date(Date.now() + this.timeLimit * 1000).toISOString()
      this.lastEvent = `life_lost_player_${player}`
      return this.getState()
    } else {
      this.lives[player] = 0
      this.endPart(player, 'timeout')
      return this.getState()
    }
  }

  accept(word) {
    this.used.add(word)
    this.current = word
    this.toMove = 1 - this.toMove
    this.turnStarted = Date.now()
    this.deadlineIso = new Date(Date.now() + this.timeLimit * 1000).toISOString()
    this.lastEvent = 'move_ok'

    if (this.availableFrom(word).length === 0) {
      this.endPart(this.toMove, 'dead_end')
      return
    }

    this.runComputer()
  }

  runComputer() {
    if (this.mode !== 'solo' || this.finished || this.toMove !== 1) {
      return
    }
    const word = this.pickComputerWord()
    if (!word) {
      this.endPart(1, 'dead_end')
      return
    }
    this.accept(word)
  }

  pickComputerWord() {
    const options = this.availableFrom(this.current)
    if (!options || options.length === 0) return null

    const pool = new Set(this.pack.levels?.[this.level] || [])
    const inLevel = options.filter((w) => pool.has(w))
    let candidateOptions = inLevel.length > 0 ? inLevel : options

    const smartChance = { basic: 0.0, intermediate: 0.5, advanced: 1.0 }[this.level] || 0.0
    if (Math.random() < smartChance) {
      let minOpponentMoves = Infinity
      for (const w of candidateOptions) {
        const remainingMoves = this.availableFrom(w).filter((x) => x !== w).length
        if (remainingMoves < minOpponentMoves) {
          minOpponentMoves = remainingMoves
        }
      }
      candidateOptions = candidateOptions.filter(
        (w) => this.availableFrom(w).filter((x) => x !== w).length === minOpponentMoves
      )
    }

    return candidateOptions[Math.floor(Math.random() * candidateOptions.length)]
  }

  endPart(loser, reason) {
    const winner = 1 - loser
    this.scores[winner] += 1
    this.lastEvent = `part_${this.part}_${reason}_loser_${loser}`

    const done = this.scores[winner] === 2 && !this.playAllParts
    if (this.part === 3 || done) {
      this.finished = true
      this.winner = this.scores[0] > this.scores[1] ? 0 : 1
      return
    }

    if (reason === 'timeout') {
      this.timeAdjustment = Math.min(this.timeAdjustment + 10, 20)
    } else if (reason === 'dead_end') {
      this.timeAdjustment = Math.max(this.timeAdjustment - 5, -10)
    }

    this.part += 1
    this.lives = [MAX_LIVES, MAX_LIVES]

    try {
      this.startPart()
    } catch (err) {
      this.finished = true
      this.winner = this.scores[0] === this.scores[1] ? null : this.scores[0] > this.scores[1] ? 0 : 1
      this.lastEvent = 'no_start_word_left'
    }
  }

  checkTurn(player) {
    if (this.finished) {
      throw new LocalGameError('match_finished', 'Le match est terminé.')
    }
    if (player !== this.toMove) {
      throw new LocalGameError('not_your_turn', "Ce n'est pas votre tour.")
    }
  }

  hint() {
    const available = this.availableFrom(this.current)
    if (!available || available.length === 0) {
      return {
        hint_type: 'exhausted',
        word_length: this.current.length,
        clue: "Attention, aucune autre transformation n'est disponible depuis ce mot !",
      }
    }

    const langDict = SYNONYMS_DB[this.lang] || {}
    const withClues = available.filter((w) => langDict[w])

    if (withClues.length > 0) {
      const target = withClues[Math.floor(Math.random() * withClues.length)]
      return {
        hint_type: 'synonym',
        word_length: target.length,
        clue: `Pense à : « ${langDict[target]} » !`,
      }
    }

    const target = available[Math.floor(Math.random() * available.length)]
    let diffIndex = 0
    for (let idx = 0; idx < this.current.length; idx++) {
      if (this.current[idx] !== target[idx]) {
        diffIndex = idx + 1
        break
      }
    }

    return {
      hint_type: 'letter_position',
      word_length: target.length,
      clue: `Essaie de modifier la lettre n°${diffIndex} pour trouver un mot valide !`,
    }
  }

  getState() {
    return {
      match_id: this.id,
      part: this.part,
      scores: [...this.scores],
      lives: [...this.lives],
      word_length: this.wordLength,
      current_word: this.current,
      to_move: this.toMove,
      time_limit: this.timeLimit,
      deadline_at: this.deadlineIso,
      used_count: this.used.size,
      finished: this.finished,
      winner: this.winner,
      event: this.lastEvent,
      is_local: true,
    }
  }
}

let activeMatch = null

export const localEngine = {
  async createMatch(lang, level, mode) {
    const pack = await loadPack(lang)
    activeMatch = new LocalMatch(pack, { lang, level, mode })
    return activeMatch.getState()
  },

  playMove(word) {
    if (!activeMatch) throw new LocalGameError('not_found', 'Aucun match actif')
    return activeMatch.play(activeMatch.toMove, word)
  },

  handleTimeout() {
    if (!activeMatch) throw new LocalGameError('not_found', 'Aucun match actif')
    return activeMatch.timeout(activeMatch.toMove)
  },

  requestHint() {
    if (!activeMatch) throw new LocalGameError('not_found', 'Aucun match actif')
    return activeMatch.hint()
  },

  getActiveMatch() {
    return activeMatch
  },

  reset() {
    activeMatch = null
  },

  clearCache() {
    packsCache.clear()
  },
}
