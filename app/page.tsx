'use client';

import { useState } from 'react';

const pricingPlans = [
  {
    id: 'onetime',
    name: 'One Time',
    price: 999,
    period: 'forever',
    description: 'Own nothing, once and for all',
    highlight: 'Best Value',
    monthlyEquivalent: null,
  },
  {
    id: 'yearly',
    name: 'Yearly',
    price: 1299,
    period: 'year',
    description: 'Annual commitment to nothingness',
    highlight: null,
    monthlyEquivalent: 108,
  },
  {
    id: 'quarterly',
    name: 'Quarterly',
    price: 399,
    period: 'quarter',
    description: 'Seasonal subscription to nothing',
    highlight: null,
    monthlyEquivalent: 133,
  },
  {
    id: 'monthly',
    name: 'Monthly',
    price: 149,
    period: 'month',
    description: 'Monthly dose of nothing',
    highlight: null,
    monthlyEquivalent: 149,
  },
  {
    id: 'weekly',
    name: 'Weekly',
    price: 49,
    period: 'week',
    description: 'Nothing, delivered weekly',
    highlight: null,
    monthlyEquivalent: 196,
  },
];

export default function Home() {
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null);

  return (
    <main className="min-h-screen flex flex-col">
      {/* Hero Section */}
      <section className="flex-1 flex flex-col items-center justify-center px-6 py-20 text-center">
        <div className="max-w-4xl mx-auto space-y-8">
          <h1 className="text-7xl md:text-8xl lg:text-9xl font-light tracking-tight text-charcoal">
            Nothing
          </h1>

          <p className="text-xl md:text-2xl font-light text-charcoal/70 max-w-2xl mx-auto">
            The most exclusive offering in existence. Pure, unadulterated nothing.
          </p>

          <div className="pt-4">
            <a
              href="#pricing"
              className="inline-block px-8 py-4 bg-charcoal text-cream font-light tracking-wider text-sm hover:bg-charcoal/90 transition-colors"
            >
              ACQUIRE NOTHING
            </a>
          </div>
        </div>
      </section>

      {/* Philosophy Section */}
      <section className="px-6 py-32 bg-charcoal text-cream">
        <div className="max-w-3xl mx-auto text-center space-y-6">
          <h2 className="text-4xl md:text-5xl font-light">
            Why Nothing?
          </h2>
          <p className="text-lg md:text-xl font-light leading-relaxed opacity-90">
            In a world consumed by excess, we offer you the ultimate luxury: absolute nothing.
            No products. No services. No clutter. Just the pure, distilled essence of emptiness.
          </p>
          <p className="text-base md:text-lg font-light leading-relaxed opacity-75">
            This is not minimalism. This is nothing.
          </p>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="px-6 py-32">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-5xl md:text-6xl font-light mb-6">
              Choose Your Nothing
            </h2>
            <p className="text-lg text-charcoal/70 font-light">
              Select your preferred investment in nothingness
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
            {pricingPlans.map((plan) => (
              <div
                key={plan.id}
                className={`relative border transition-all cursor-pointer ${
                  selectedPlan === plan.id
                    ? 'border-charcoal bg-charcoal text-cream shadow-2xl scale-105'
                    : 'border-charcoal/20 hover:border-charcoal/40 bg-cream'
                }`}
                onClick={() => setSelectedPlan(plan.id)}
              >
                {plan.highlight && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gold text-cream px-4 py-1 text-xs tracking-widest">
                    {plan.highlight}
                  </div>
                )}

                <div className="p-8 space-y-6">
                  <div className="space-y-2">
                    <h3 className="text-sm tracking-widest font-light opacity-70 uppercase">
                      {plan.name}
                    </h3>
                    <div className="space-y-1">
                      <div className="text-4xl font-light">
                        ${plan.price}
                      </div>
                      <div className="text-sm opacity-60">
                        per {plan.period}
                      </div>
                    </div>
                  </div>

                  {plan.monthlyEquivalent && (
                    <div className="text-xs opacity-50 border-t border-current pt-4">
                      ~${plan.monthlyEquivalent}/mo equivalent
                    </div>
                  )}

                  <p className="text-sm font-light leading-relaxed opacity-80 min-h-[3rem]">
                    {plan.description}
                  </p>

                  <button
                    className={`w-full py-3 text-sm tracking-widest transition-colors ${
                      selectedPlan === plan.id
                        ? 'bg-cream text-charcoal'
                        : 'bg-charcoal text-cream hover:bg-charcoal/90'
                    }`}
                  >
                    SELECT
                  </button>
                </div>
              </div>
            ))}
          </div>

          {selectedPlan && (
            <div className="mt-16 text-center space-y-6 max-w-2xl mx-auto">
              <p className="text-lg font-light text-charcoal/70">
                You have selected:{' '}
                <span className="text-charcoal font-normal">
                  {pricingPlans.find(p => p.id === selectedPlan)?.name} Plan
                </span>
              </p>
              <button className="px-12 py-5 bg-charcoal text-cream text-sm tracking-widest hover:bg-charcoal/90 transition-colors">
                PROCEED TO NOTHINGNESS
              </button>
              <p className="text-xs text-charcoal/50 font-light">
                By purchasing nothing, you agree to receive absolutely nothing in return.
              </p>
            </div>
          )}
        </div>
      </section>

      {/* What You Get Section */}
      <section className="px-6 py-32 bg-charcoal/5">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-light text-center mb-16">
            What You Receive
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="text-center space-y-4">
              <div className="text-6xl font-light text-gold">∅</div>
              <h3 className="text-xl font-light">Nothing Physical</h3>
              <p className="text-sm font-light text-charcoal/70 leading-relaxed">
                Zero products will be shipped. Your carbon footprint remains pristine.
              </p>
            </div>

            <div className="text-center space-y-4">
              <div className="text-6xl font-light text-gold">∞</div>
              <h3 className="text-xl font-light">Infinite Possibility</h3>
              <p className="text-sm font-light text-charcoal/70 leading-relaxed">
                With nothing comes everything. The void is your canvas.
              </p>
            </div>

            <div className="text-center space-y-4">
              <div className="text-6xl font-light text-gold">−</div>
              <h3 className="text-xl font-light">Complete Freedom</h3>
              <p className="text-sm font-light text-charcoal/70 leading-relaxed">
                No maintenance. No updates. No obsolescence. Pure liberation.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-12 border-t border-charcoal/10">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-sm font-light text-charcoal/50 tracking-wide">
            © 2024 Nothing. All rights reserved. Which is to say, no rights reserved. Because there is nothing.
          </p>
        </div>
      </footer>
    </main>
  );
}
