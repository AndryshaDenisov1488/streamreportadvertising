import React from 'react'

/** Статика из `public/` — попадает в корень `dist` при сборке */
export const MAINSTREAM_LOGO_SRC = '/mainstream-logo.png'

type BrandLogoProps = {
  /** Высота логотипа, ширина подбирается автоматически */
  height?: number
  className?: string
  style?: React.CSSProperties
}

export const BrandLogo: React.FC<BrandLogoProps> = ({ height = 32, className, style }) => (
  <img
    className={className}
    src={MAINSTREAM_LOGO_SRC}
    alt="MainStream"
    height={height}
    decoding="async"
    draggable={false}
    style={{
      display: 'block',
      objectFit: 'contain',
      objectPosition: 'left center',
      width: 'auto',
      maxWidth: 'min(100%, 280px)',
      height,
      ...style,
    }}
  />
)
