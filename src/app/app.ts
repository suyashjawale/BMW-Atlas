import { Component, computed, HostListener, signal } from '@angular/core';
import { BikeDataMap } from './interface/bike-data-map';
import { HttpClient } from '@angular/common/http';

@Component({
	selector: 'app-root',
	imports: [],
	templateUrl: './app.html',
	styleUrl: './app.scss'
})
export class App {
	Math = Math;
	model_data = signal<BikeDataMap>({});
	models = computed(() =>
		Object.keys(this.model_data()).map(key => ({
			modelName: key,
			img: this.model_data()[key].locations[0].imageName,
			segment: this.model_data()[key].segment
		}))
	);
	total_models = computed(() => this.models().length);
	currentIndex = signal(0);
	showImages = signal(false);
	private imageTimer: any;

	constructor(private http: HttpClient) { }

	ngOnInit() {
		this.http.get<BikeDataMap>('modelList.json').subscribe(data => {
			const entries = Object.entries(data);

			// 2. Shuffle the pairs using the sort hack
			entries.sort(() => Math.random() - 0.5);

			// 3. Reconstruct into an object and update signal
			this.model_data.set(Object.fromEntries(entries));
			this.scheduleImageLoad();
		});
	}

	visibleItems = computed(() => {
		const current = this.currentIndex();
		const total = this.total_models();
		const buffer = [];

		for (let i = -10; i <= 10; i++) {
			const index = (current + i + total) % total;
			buffer.push({
				label: this.models()[index],
				index,
				offset: i
			});
		}

		return buffer;
	});

	private scheduleImageLoad() {
		this.showImages.set(false);
		clearTimeout(this.imageTimer);
		this.imageTimer = setTimeout(() => this.showImages.set(true), 300);
	}

	select(index: number) {
		this.currentIndex.set(index);
		this.scheduleImageLoad();
	}

	next() {
		this.currentIndex.update(i => (i + 1) % this.total_models());
		this.scheduleImageLoad();
	}

	prev() {
		this.currentIndex.update(i => (i - 1 + this.total_models()) % this.total_models());
		this.scheduleImageLoad();
	}

	// ⌨️ keyboard
	@HostListener('window:keydown', ['$event'])
	onKey(e: KeyboardEvent) {
		if (e.key === 'ArrowRight') this.next();
		if (e.key === 'ArrowLeft') this.prev();
	}

	// ✅ Fix 5: swipe support
	private touchStartX = 0;

	@HostListener('touchstart', ['$event'])
	onTouchStart(e: TouchEvent) {
		this.touchStartX = e.touches[0].clientX;
	}

	@HostListener('touchend', ['$event'])
	onTouchEnd(e: TouchEvent) {
		const delta = this.touchStartX - e.changedTouches[0].clientX;
		if (Math.abs(delta) > 50) {
			delta > 0 ? this.next() : this.prev();
		}
	}

	openLink(link: string) {
		window.open(link);
	}
}
