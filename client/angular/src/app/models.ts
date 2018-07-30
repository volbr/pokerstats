export interface Team {
  id: number,
  name: string,
  players?: Player[]
}

export interface Player {
  id: number,
  name: string,
  team?: Team,
  game?: number
}

export interface Round {
  id: number,
  winner: any,
  combination: any,
  winning: number,
}

export interface Stats {
  user: number,
  username: string,
  win_total: number,
  wins: number,
  rebuy_total: number,
  rebuys: number,
  total: number
}

export interface GameResult {
  id?: number,
  game: number,
  player: Player,
  stake: number,
  rebuy?: number,
  profit?: number,
  best_combination?: Round,
  best_winning?: Round
}

export interface Game {
  id?: number,
  creator?: number,
  round?: number,
  rounds?: Round[],
  stats?: Stats[],
  players?: any[],
  init_stake?: number,
  team?: number,
  results?: GameResult[],
  best_result?: GameResult,
  best_combination?: Round,
  best_winning?: Round,
  created?: Date,
  finished?: Date,
  // Sets by games component
  selected?: number

}

export interface Rebuy {
  player: number,
  amount: number,
  round: number
}
