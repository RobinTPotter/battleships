
function Vector() {
	//console.log("Vector",arguments)
	if (arguments.length==2) {
		this.x=arguments[0]
		this.y=arguments[1]
	} else {
		this.x=0
		this.y=0
	}
	this.magnitude=vector_magnitude
	this.angle=vector_angle
	this.octant=vector_octant
	this.normalize=vector_normalize
	this.distance=vector_distance
	this.add=vector_add
	this.subtract=vector_subtract
	this.string=vector_string
	this.rotate=vector_rotate
	this.anglebetween=vector_anglebetween
	this.scalarproduct=vector_scalarproduct
	this.scalardiff=vector_scalardiff
	this.multiply=vector_multiply
	this.magnitudecap=vector_magnitudecap

}
function vector_multiply(s) {
	return new Vector(this.x*s,this.y*s)
}
function vector_distance(v) {
	return Math.sqrt (  (this.x-v.x)*(this.x-v.x) + (this.y-v.y)*(this.y-v.y)  )
}
function vector_add(v) {
	return new Vector(this.x+v.x,this.y+v.y)
}
function vector_subtract(v) {
	return new Vector(this.x-v.x,this.y-v.y)
}
function vector_string() {
	return Math.round(this.x,0.001)+','+Math.round(this.y,0.001)
}
function vector_magnitude() {
	var x=Math.sqrt(this.x*this.x + this.y*this.y)
	return x
}
function vector_magnitudecap(c) {
	var m=this.magnitude()
	if (Math.abs(m)>c) {
		var sign=m/Math.abs(m)
		m=c*sign
		return this.normalize().multiply(m)
	} else return this
}

function vector_angle() {
	if (this.y==0) {
		if (this.x>0) return 0; else return Math.PI;
	} else if (this.x==0) {
		if (this.y>0) return Math.PI/2; else return 3*Math.PI/2;
	} else {
		var ang=Math.abs(Math.atan(this.y/this.x));
		if (this.x>0 & this.y>0) return ang
		else if (this.x>0 & this.y<0) return 2*Math.PI-ang
		else if (this.x<0 & this.y>0) return Math.PI-ang
		else if (this.x<0 & this.y<0) return Math.PI+ang
	}
}
function vector_anglebetween(v) {
	var an1=this.angle()
	var an2=v.angle()
	var diff=0
	if (an1>an2) diff=Math.abs(an1-an2); else diff=Math.abs(an2-an1);
	if (diff>Math.PI) diff=2*Math.PI-diff
	return diff
}
function vector_rotate(angle) {
	var m=new Matrix(Math.cos(angle),-Math.sin(angle),Math.sin(angle),Math.cos(angle))
	return new Vector(this.x * m.a + this.y * m.c, this.x * m.b + this.y * m.d)
}
function vector_octant() {
	var ang=this.angle()-Math.PI/8
	if (ang<0) ang=ang+2*Math.PI
	ang=Math.ceil(8*(ang)/(2*Math.PI))
	if (ang>7) ang=0
	return ang
}
function vector_normalize() {
	var mag=this.magnitude()
	return new Vector(this.x/mag,this.y/mag)
}
function vector_scalarproduct(v) {
	return this.x*v.x+this.y*v.y
}
function vector_scalardiff(v) {
	return this.x*v.x-this.y*v.y
}
function line_point_test(l1,l2,p3) {
     return ((l2.x - l1.x)*(p3.y - l1.y) - (l2.y - l1.y)*(p3.x - l1.x)) > 0
}
