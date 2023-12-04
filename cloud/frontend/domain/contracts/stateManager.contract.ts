type Function<K> = (arg: K) => void;

export type StateManager<T> = [T, Function<T>];
