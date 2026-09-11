export function SynapseArtwork() {
  // Placeholder pending real commissioned neuron/synapse artwork (DESIGN.md §5).
  // Abstract branches and nodes are decorative, not an anatomical visualization.
  return (
    <svg aria-hidden="true" focusable="false" viewBox="0 0 560 760" preserveAspectRatio="xMidYMid slice" className="absolute inset-0 h-full w-full">
      <defs>
        <linearGradient id="synapse-ground" x1="0" y1="1" x2="1" y2="0">
          <stop className="[stop-color:theme(colors.brand.navy)]" />
          <stop offset="1" className="[stop-color:theme(colors.brand.indigo)]" />
        </linearGradient>
      </defs>
      <path fill="url(#synapse-ground)" d="M0 0h560v760H0z" />
      <g fill="none" strokeLinecap="round" strokeLinejoin="round">
        <g className="stroke-brand-violet" strokeWidth="1.5" opacity="0.55">
          <path d="M-50 210C65 206 108 220 180 320S293 419 352 390 442 245 600 273" />
          <path d="M-50 228C60 222 112 241 169 328S299 441 360 406 457 264 600 291" />
          <path d="M-50 246C50 240 101 251 157 337S305 461 369 423 468 283 600 309" />
          <path d="M-50 264C43 258 90 265 145 346S310 481 378 440 483 302 600 327" />
          <path d="M-50 282C36 276 79 279 133 355S316 501 387 457 498 321 600 345" />
        </g>
        <g className="stroke-brand-teal" strokeWidth="2">
          <path d="M-24 535C79 524 113 478 191 385C211 357 229 335 256 307" />
          <path d="M191 385C147 352 105 335 69 298L28 249M69 298L21 315M105 335L105 285" />
          <path d="M256 307C292 259 333 226 374 195L414 136M374 195L444 197M333 226L331 167" />
          <path d="M256 307C232 262 207 229 208 177L189 119M208 177L251 136M222 245L163 222" />
          <path d="M256 307C306 320 339 340 385 322L440 299M385 322L416 361M339 340L331 383" />
          <path d="M87 497L100 565 71 624M100 565L155 601" />
        </g>
        <g className="stroke-brand-violet" strokeWidth="2.5">
          <path d="M602 674C500 660 459 601 391 519C367 490 347 474 320 459" />
          <path d="M320 459C276 452 236 472 204 503L157 531M204 503L217 553M260 468L244 422" />
          <path d="M320 459C321 411 351 378 376 363L387 410M376 363L431 384M351 378L342 355" />
          <path d="M391 519C424 493 444 457 476 442L530 425M476 442L477 389M444 457L427 425" />
          <path d="M391 519C369 562 347 585 348 627L328 677M348 627L394 661M358 583L309 588" />
          <path d="M486 625L501 562 533 531M501 562L481 543" />
        </g>
      </g>
      <g className="fill-brand-teal">
        {[[28,249],[21,315],[105,285],[414,136],[444,197],[331,167],[189,119],[251,136],[163,222],[440,299],[416,361],[331,383],[71,624],[155,601]].map(([cx, cy]) => <circle key={`${cx}-${cy}`} cx={cx} cy={cy} r="4" />)}
        <circle cx="191" cy="385" r="6" />
        <circle cx="256" cy="307" r="12" />
        <circle cx="256" cy="307" r="25" fill="none" className="stroke-brand-teal" opacity="0.35" />
      </g>
      <g className="fill-brand-violet">
        {[[157,531],[217,553],[244,422],[387,410],[431,384],[342,355],[530,425],[477,389],[427,425],[328,677],[394,661],[309,588],[533,531],[481,543]].map(([cx, cy]) => <circle key={`${cx}-${cy}`} cx={cx} cy={cy} r="4" />)}
        <circle cx="391" cy="519" r="6" />
        <circle cx="320" cy="459" r="12" />
        <circle cx="320" cy="459" r="25" fill="none" className="stroke-brand-violet" opacity="0.5" />
      </g>
      {/* One warm highlight, as specified by the Brand palette. */}
      <circle cx="256" cy="307" r="5" className="fill-brand-amber" />
    </svg>
  );
}
