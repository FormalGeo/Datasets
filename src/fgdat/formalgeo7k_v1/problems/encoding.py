geo_sym = [
    "△",  # triangle
    "∠",  # angle
    "⊙",  # circle
    "▱",  # parallelogram
    "°",  # degree
    "∥",  # parallel
    "⊥",  # perpendicular
    "⌒",  # arc
    "²",  # pow
]

greek_alp = [
    'Α', 'α',  # a:lf
    'Β', 'β',  # bet
    'Γ', 'γ',  # ga:m
    'Δ', 'δ',  # delt
    'Ε', 'ε',  # ep`silon
    'Ζ', 'ζ',  # zat
    'Η', 'η',  # eit
    'Θ', 'θ',  # θit
    'Ι', 'ι',  # aiot
    'Κ', 'κ',  # kap
    'Λ', 'λ',  # lambd
    'Μ', 'μ',  # mju
    'Ν', 'ν',  # nju
    'Ξ', 'ξ',  # ksi
    'Ο', 'ο',  # omik`ron
    'Π', 'π',  # pai
    'Ρ', 'ρ',  # rou
    'Σ', 'σ',  # sigma
    'Τ', 'τ',  # tau
    'Υ', 'υ',  # jup`silon
    'Φ', 'φ',  # fai
    'Χ', 'χ',  # phai
    'Ψ', 'ψ',  # psai
    'Ω', 'ω'  # o`miga
]


def show_unicode(char):
    print(hex(ord(char)))


if __name__ == '__main__':
    show_unicode('🤡')
